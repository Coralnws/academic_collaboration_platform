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



#createReview
#getReview

# @csrf_exempt
# def createArticleReview(request):
#     if request.method == 'POST':
#         userId = request.POST.get('userId')
#         articleId = request.POST.get('paperId')
#         content = request.POST.get('content')
#         user = CustomUser.objects.filter(id=userId).first()

#         newReview = Review(article=articleId,content=content,createdBy=user)
#         newReview.save()

#         data = searchPaperAuthor(articleId)
            
#         name = data[0]
#         print("name:"+name)
#         authorList = data[1]

#         for tmp in authorList:
#             if 'id' in tmp: 
#                 scholarUser = CustomUser.objects.filter(scholarAuth=tmp['id']).first()
#                 newNotice = Notification(type=10,belongTo=scholarUser,userId=userId,userName=user.username,paperId=articleId,paperName=name)
#                 newNotice.save()

#         return UTF8JsonResponse({'errno':1001, 'msg': '成功发布评论'})

@csrf_exempt
def createReview(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        reviewId = request.POST.get('reviewId')
        paperId = request.POST.get('paperId')
        content = request.POST.get('content')

        user = CustomUser.objects.filter(id=userId).first()
        
        if user.banComment:
            if user.banDuration > timezone.now():
                data={}
                data['banDuration'] = user.banDuration
                return UTF8JsonResponse({'errno':3001, 'msg': '用户已被禁言','data':data})
            else:
                user.banComment=False
                user.banDuration=None
        if reviewId is not None:
            review = Review.objects.filter(id=reviewId).first()

            notifyUser = review.createdBy

            data = searchPaperAuthor(paperId)
            name = data[0]

            newReview = Review(review=review,content=content,createdBy=user)
            newReview.save()
                
            newNotice = Notification(type=11,belongTo=notifyUser,userId=userId,userName=user.username,paperId=paperId,paperName=name,reviewId=reviewId)
            newNotice.save()

            data={}
            data['newReviewId'] = newReview.id 
            data2=model_to_dict(newNotice)
            return UTF8JsonResponse({'errno':1001, 'msg': '成功回复评论','review':data,'notification':data2})
        else:
            newReview = Review(article=paperId,content=content,createdBy=user)
            newReview.save()

            data = searchPaperAuthor(paperId)
                
            name = data[0]
            print("name:"+name)
            authorList = data[1]

            for tmp in authorList:
                if 'id' in tmp: 
                    scholarUser = CustomUser.objects.filter(scholarAuth=tmp['id']).first()
                    newNotice = Notification(type=10,belongTo=scholarUser,userId=userId,userName=user.username,paperId=paperId,paperName=name)
                    newNotice.save()

            data={}
            data['newReviewId'] = newReview.id 
            data2=model_to_dict(newNotice)
            return UTF8JsonResponse({'errno':1001, 'msg': '成功发布评论','review':data,'notification':data2})


@csrf_exempt
def getReview(request):
    if request.method == 'GET':
        paperId = request.GET.get('paperId','')
        reviewId = request.GET.get('reviewId','')
        
        
        if paperId:
            reviewList = Review.objects.filter(article=paperId) 
        if reviewId:
            belongToReview = Review.objects.filter(id=reviewId).first()
            reviewList = Review.objects.filter(review=belongToReview) 
        
        data = []
        for tmp in reviewList:
            data1 = model_to_dict(tmp)
            data1['id']=tmp.id
            data.append(data1)
            print(data1)

        return UTF8JsonResponse({'errno':1001, 'msg': '返回评论成功', 'data': data})

@csrf_exempt
def reportReview(request):
    if request.method == 'POST':
        # userId=request.session.get('uid')
        # if userId is None:
        #     return UTF8JsonResponse({'errno': 800001, 'msg': '当前cookie为空，未登录，请先登录'})
        userId = request.POST.get('userId')
        print(userId)
        reviewId = request.POST.get('reviewId')
        print(reviewId)
        type = request.POST.get('type')
        user = CustomUser.objects.filter(id=userId).first()
        print(user)
        review = Review.objects.filter(id=reviewId).first()

        newReport = ReviewReport(reportReview=review,category=type,createdBy=user)

        newReport.save()

        data=model_to_dict(newReport)
        
        return UTF8JsonResponse({'errno':1001, 'msg': '成功举报评论','data':data})


@csrf_exempt
def manageReviewReport(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        userStaff = CustomUser.objects.filter(id=userId).first()
        if userStaff.is_staff == False:
            return UTF8JsonResponse({'errno':3001, 'msg': '非管理员'})
        reportId = request.POST.get('reportId')
        report=ReviewReport.objects.filter(id=reportId).first()
        review = report.reportReview
        user = CustomUser.objects.filter(id=review.createdBy.id).first()
        
        result = request.POST.get('result') #0=decline ,1=accept
        articleId = review.article
        data = searchPaperAuthor(articleId)
            
        name = data[0]
        if result == '1':
            user.banComment = True
            user.banDuration = timezone.now() + timezone.timedelta(days=3)
            user.save()
            report.result=True
            noticeToCreator = Notification(type=12,belongTo=user,paperId=articleId,paperName=name)
            noticeToCreator.save()
            noticeToUser = Notification(type=13,belongTo=report.createdBy,paperId=articleId,paperName=name,userId=user.id,userName=user.username)
            noticeToUser.save()

            review.delete()
            data=model_to_dict(noticeToUser)
            data1=model_to_dict(noticeToCreator)
            return UTF8JsonResponse({'errno':1001, 'msg': '举报通过，已将用户禁言三天','noticeToReviewCreator':data1,'noticeToReportCreator':data})
        elif result == '0':
            report.result=False
            noticeToUser = Notification(type=14,belongTo=report.createdBy,paperId=articleId,paperName=name,userId=user.id,userName=user.username)
            noticeToUser.save()
            data=model_to_dict(noticeToUser)
            return UTF8JsonResponse({'errno':2001, 'msg': '举报驳回','notification':data})


@csrf_exempt
def deleteReview(request):
    if request.method == 'POST':
        reviewId=request.POST.get('reviewId')
        userId = request.POST.get('userId')
        review = Review.objects.filter(id=reviewId).first()
        user= CustomUser.objects.filter(id=userId).first()
        if review.createdBy==user:
            review.delete()
            return UTF8JsonResponse({'errno':1001, 'msg': '成功删除评论'})
        else:
            return UTF8JsonResponse({'errno':2001, 'msg': '非本人操作'})
