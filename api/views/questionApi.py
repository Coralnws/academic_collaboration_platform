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
from django.forms.models import model_to_dict

@csrf_exempt
def createQuestionReply(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        scholarId = request.POST.get('scholarId')
        type = request.POST.get('type') #0=新建问题 ， 1=回答或追问
        content = request.POST.get('content')
        user = CustomUser.objects.filter(id=userId).first()
        newQuestion=None
        if(type=="0"):
            newQuestion = Question(createdBy=user,scholar=scholarId,category=type,content=content)
            newQuestion.content = request.POST.get('content')
            newQuestion.save()
        else: #追问的话，前端传来主问题的id
            existQuestion = Question.objects.filter(id=request.POST.get('mainQuestion')).first()
            newQuestion = Question(createdBy=user,scholar = scholarId , category=type,belongToQuestion=existQuestion,content=content)
            newQuestion.content = request.POST.get('content')
            newQuestion.save()

        data=model_to_dict(newQuestion)
        return JsonResponse({'errno':1001, 'msg': '成功提问','question':data})

@csrf_exempt
def getQuestionReply(request):
    if request.method == 'GET':
        scholarId = request.GET.get('scholarId','')
        print(scholarId)
        type = request.GET.get('type','')

        if type == "0":
            questionList = Question.objects.filter(scholar=scholarId,category=type).order_by('createdAt')

        if type == "1":
            mainQuestion = Question.objects.filter(id=request.GET.get('mainQuestion','')).first()
            questionList = Question.objects.filter(scholar=scholarId,category=type,belongToQuestion=mainQuestion).order_by('createdAt')

        data = []
        for tmp in questionList:
            data1 = model_to_dict(tmp)
            data1['id']=tmp.id
            data.append(data1)
            print(data1)

        return JsonResponse({'errno':1001, 'msg': '获取提问信息', 'data': data})