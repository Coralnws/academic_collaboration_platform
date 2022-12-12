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

def showScholarPage(request):
    if request.method == 'GET':
        scholarId = request.GET.get('scholarId','')
        result = searchAuthor(scholarId)
        return UTF8JsonResponse({'errno':1001, 'msg': '返回学者信息','data':result})
        