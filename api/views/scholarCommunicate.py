from datetime import timedelta
from datetime import datetime
import time
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils import timezone
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from api.models import *
from ..utils import *
from api.search import *
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from django.core import serializers

#关注 - followScholar(POST,follow and unfollow) , listFollow(GET) , 
#提问/追问追答 - 在学者门户显示出来，拿学者id来分别，
#       createQuestionReply(POST & category depands on sender type),listQuestionReply(GET & sort by createdTime)
#私信 - requestPrivateMessage(by user) , getRequest(by scholarUser) , replyRequest(by scholarUser) , getMessage()(combine both user and sort by time) 
#       createMessage 
#getMessage的时候可以把message都link去某个学者和user的连接通道，这样的话就通过两个user找
#查看学者门户 - 直接返回一个学者信息

#UserRequestScholar 相当于连接通道，sendRequest就是create一个通道，然后设成0已发送，getRequest的时候就找type=0的，
#发送私信请求，有学者身份的user get私信请求，回复私信请求， 检查当前user和目标学者的通信情况，get两个user之间的信息记录
@csrf_exempt
def followScholar(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        scholarId = request.POST.get('scholarId')
        scholarName = request.POST.get('scholarName')
        user = CustomUser.objects.filter(id=userId).first()
        print(scholarId)
        
        userScholar = UserScholar.objects.filter(user=user,scholar=scholarId).first()
        scholarUser = CustomUser.objects.filter(scholarAuth=scholarId).first()
        print(scholarUser)
        
        if userScholar is None:
            newFollow = UserScholar(user=user,scholar=scholarId,scholarName=scholarName)
            newFollow.isFollow = True
            newFollow.save()
            if scholarUser:
                newNotice = Notification(type=1,belongTo=scholarUser,userId=userId,userName=user.username,scholarId=scholarId,scholarName=scholarName)
                newNotice.save()
                

            return JsonResponse({'errno': 1001, 'msg': "成功关注学者"})
        else:
            if userScholar.isFollow == True:
                userScholar.isFollow = False
            else:
                userScholar.isFollow = True
                if scholarUser:
                    newNotice = Notification(type=1,belongTo=scholarUser,userId=userId,userName=user.username,scholarId=scholarId,scholarName=scholarName)
                    newNotice.save()

            userScholar.save()    
    
            return JsonResponse({'errno': 1001, 'msg': "成功关注/取关学者"})
        
@csrf_exempt
def getFollowList(request): #get scholarName by id and return 
    if request.method == 'GET':
        userId = request.GET.get('userId','')
        print(userId)
        user = CustomUser.objects.filter(id=userId).first()
        
        followList=[]
        
        userScholarList = UserScholar.objects.filter(user=user,isFollow=True)

        data = []
        for tmp in userScholarList:
            data1 = model_to_dict(tmp)
            data1['id']=tmp.id
            data.append(data1)

        return JsonResponse({'errno':1001, 'msg': '返回关注列表成功', 'data': data})
            

@csrf_exempt
def createQuestionReply(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        scholarId = request.POST.get('scholarId')
        type = request.POST.get('type') #0=新建问题 ， 1=用户后来追问， 2=学者回答
        user = CustomUser.objects.filter(id=userId).first()
        if(type=="0"):
            newQuestion = Question(createdBy=user,scholar = scholarId , category=type)
            newQuestion.content = request.POST.get('content')
            newQuestion.save()
        else: #追问的话，前端传来主问题的id
            existQuestion = Question.objects.filter(id=request.POST.get('mainQuestion'))
            newQuestion = Question(createdBy=user,scholar = scholarId , category=type,belongQuestion=existQuestion)
            newQuestion.content = request.POST.get('content')
            newQuestion.save()
    

@csrf_exempt
def requestPrivateMessage(request):
    if request.method == 'POST':
        user = CustomUser.objects.filter(id=request.POST.get('userId')).first()
        scholar = CustomUser.objects.filter(scholarAuth = request.POST.get('scholarId')).first()
        existRequest = UserRequestScholar.objects.filter(user=user,scholar=scholar)
        if existRequest:
            existRequest.status=0
        else:
            request = UserRequestScholar(user=user,scholar=scholar,status=1)
            request.save()

        # notification = user.username + " 已向您发起私信请求。"
        # newNotice = Notification(user=scholar,content=notification)
        # newNotice.save()

        return JsonResponse({'errno': 1001, 'msg': "成功要求私信"})

@csrf_exempt
def getRequest(request): #getChatBox
    if request.method == 'GET':
        userId = request.GET.get('userId','')
        #type = request.GET.get('type','') #0=pending 1=chatbox
        user = CustomUser.objects.filter(id=userId).first()
        requestList = UserRequestScholar.objects.filter(scholar=user,status=1)
        data = []
        for tmp in requestList:
            count = Message.objects.filter(userRequestScholar=tmp,seen=False).count()
            tmp.unread = count
            lastMessage = Message.objects.filter(userRequestScholar=tmp).order_by('-createdAt').first()
        
            data1 = model_to_dict(tmp)
            data1['id']=tmp.id
            if lastMessage:
                data1['lastMessageContent']=lastMessage.content
                data1['lastMessageTime']=lastMessage.createdAt
                if lastMessage.sentBy == user:
                    data1['lastMessageSentFrom'] = 0
                else:
                    data1['lastMessageSentFrom'] = 1
            else:
                data1['lastMessageContent']= None
                data1['lastMessageTime']=None 
            data.append(data1)
        
        return JsonResponse({'errno':1001, 'msg': '返回数据成功', 'data': data})

@csrf_exempt
def replyRequest(request):
    if request.method == 'POST':
        # uid=request.session.get('uid')
        # if uid is None:
        #     return JsonResponse({'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
        userId = request.POST.get('userId')
        user = CustomUser.objects.filter(id=userId).first()
        requestId = request.POST.get('requestId')
        status = request.POST.get('type') #0=reject,1=accept
        userRequest= UserRequestScholar.objects.filter(id=requestId).first()
        notification=""
        if(status == "0"):
            userRequest.status = 2
            notification = user.username + " 已拒绝了您的私信请求。"
            newNotice = Notification(user=userRequest.user,content=notification,chat=userRequest)
        elif(status == "1"):
            userRequest.status = 1
            notification = user.username + " 已接受了您的私信请求。"
            newNotice = Notification(user=userRequest.user,content=notification)

        userRequest.save()
        newNotice.save()
    
        return JsonResponse({'errno':1001, 'msg': '回复请求成功'})


@csrf_exempt
def getChatBoxMessage(request):
    if request.method == 'GET':
        userId = request.GET.get('userId','')
        user = CustomUser.objects.filter(id=userId).first()
        chatBoxId = request.GET.get('chatBoxId','')
        chatBox = UserRequestScholar.objects.filter(id=chatBoxId).first()
        messageList = Message.objects.filter(userRequestScholar=chatBox)

        data = []
        for tmp in messageList:
            if tmp.sentBy == user:
                tmp.sentFrom = 0
            else:
                tmp.sentFrom = 1

            data1 = model_to_dict(tmp)
            data1['id']=tmp.id
            data.append(data1)
            tmp.seen = True
            tmp.save()
    
        return JsonResponse({'errno':1001, 'msg': '返回信息数据成功', 'data': data})

@csrf_exempt
def sendMessage(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        user = CustomUser.objects.filter(id=userId)
        chatBoxId = request.POST.get('chatBoxId')
        chatBox = UserRequestScholar.objects.filter(id=chatBoxId).first()
        content = request.POST.get('content')
        user = CustomUser.objects.filter(id=userId).first()
        message = Message(sentBy=user,content=content,userRequestScholar=chatBox)
        message.save()

        # if chatBox.user == user:
        #     target = CustomUser.objects.filter(id=chatBox.scholar.id).first()
        # else:
        #     target = CustomUser.objects.filter(id=chatBox.user.id).first()

        # # notification = "您有来自 " + user.username + " 的新消息"
        # # existNotification = Notification.objects.filter(user=target,content=notification).first()
        # # if existNotification is None:
        # #     notification = "您有来自 " + user.username + " 的新消息"
        # #     newNotice = Notification(user=target,content=notification,chat=chatBox)
        # #     newNotice.save()

        return JsonResponse({'errno':1001, 'msg': '发送信息成功'})

@csrf_exempt
def getAuthorListFromEs(request):
    if request.method == 'GET':
        scholar_name = request.GET.get('name')
        
        authorList = searchAuthor(scholar_name)

        return JsonResponse(authorList,safe=False)

