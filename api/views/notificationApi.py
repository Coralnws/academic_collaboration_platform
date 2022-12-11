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
from django.db.models import Q


#getNotification 
@csrf_exempt
def getNotification(request):
    if request.method == 'GET':
        userId = request.GET.get('userId','')
        user = CustomUser.objects.filter(id=userId).first()

        notificationList = Notification.objects.filter(belongTo=user)
        data = []
        for tmp in notificationList:
            data1 = model_to_dict(tmp)
            data1['id']=tmp.id
            data.append(data1)
            print(data1)
            tmp.seen = True
            tmp.save()

        return JsonResponse({'errno':1001, 'msg': '返回通知列表成功', 'data': data})
            
@csrf_exempt
def checkNotification(request):
    if request.method == 'GET':
        userId = request.GET.get('userId','')
        user = CustomUser.objects.filter(id=userId).first()
    #notification and chatBox
    count = 0
    notificationCount = Notification.objects.filter(belongTo=user,seen=False).count()
    chatBox = UserRequestScholar.objects.filter(Q(user=user) | Q(scholar=user))
    unreadMessage = 0
    for tmp in chatBox:
        unreadMessage = Message.objects.filter(userRequestScholar=tmp,seen=False).count()
        if unreadMessage > 0:
            break

    count = notificationCount + unreadMessage
    return JsonResponse({'count': count})
    
    


