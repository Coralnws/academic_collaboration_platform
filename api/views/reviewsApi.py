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

@csrf_exempt
def createArticleReview(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        articleId = request.POST.get('paperId')
        content = request.POST.get('content')
        user = CustomUser.objects.filter(id=userId).first()

        newReview = Review(article=articleId,content=content,createdBy=user)
        newReview.save()

        data = searchPaperAuthor(articleId)
            
        name = data[0]
        print("name:"+name)
        authorList = data[1]

        for tmp in authorList:
            if 'id' in tmp: 
                scholarUser = CustomUser.objects.filter(scholarAuth=tmp['id']).first()
                newNotice = Notification(type=6,belongTo=scholarUser,userId=userId,userName=user.username,paperId=articleId,paperName=name)
                newNotice.save()

        return JsonResponse({'errno':1001, 'msg': '成功发布评论'})

@csrf_exempt
def replyReview(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        reviewId = request.POST.get('reviewId')
        paperId = request.POST.get('paperId')
        content = request.POST.get('content')

        user = CustomUser.objects.filter(id=userId).first()
        review = Review.objects.filter(id=reviewId).first()

        notifyUser = review.createdBy

        data = searchPaperAuthor(paperId)
        name = data[0]

        newReview = Review(review=review,content=content,createdBy=user)
        newReview.save()

        # article = review.paperId
        # while article is None:
        #     review = review.review
        #     article = review.paperId
            
        newNotice = Notification(type=7,belongTo=notifyUser,userId=userId,userName=user.username,paperId=paperId,paperName=name,reviewId=reviewId)
        newNotice.save()

        return JsonResponse({'errno':1001, 'msg': '成功回复评论'})

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

        return JsonResponse({'errno':1001, 'msg': '返回评论成功', 'data': data})

