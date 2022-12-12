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

@csrf_exempt
def requestScholarAuthenticate(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        scholarId = request.POST.get('scholarId')
        user = CustomUser.objects.filter(id=userId).first()
        #scholar = request.POST.get('scholar_name')
        scholar = Scholar.objects.filter(id=scholarId).first()
        scholar_name = scholar.name.replace(" ", "")
        if scholar.belongTo is not None:
            return UTF8JsonResponse({'errno': 3003, 'msg': "学者已被认领"})
        
        if user:
            match = False
            names = user.real_name.split(' ')
            for name in names:
                if name in scholar_name:
                    match = True

            if match:
                genCode = gen_code()
                oldCode = Code.objects.filter(sendTo=user).first()
                if oldCode:
                    oldCode.code = genCode
                    oldCode.updatedAt = timezone.now()
                    oldCode.save()
                else:
                    code = Code()
                    code.code = genCode
                    code.sendTo = user
                    code.save()
                #(user,scholar_name,request,code,subject, fileName)
                send_smtp(user,scholar,request,genCode,"Scholar Authentication 认领学者身份","authenticate_scholar.txt")
                return UTF8JsonResponse({'errno': 1001, 'msg': "邮件已发送"})
            else:
                return UTF8JsonResponse({'errno': 3002, 'msg': "用户名与学者名不符"})

        else:
            return UTF8JsonResponse({'errno': 3001, 'msg': "用户不存在"})

@csrf_exempt
def validateScholarAuthentication(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        code = request.POST.get('code')
        scholarId = request.POST.get('scholarId')
        user = CustomUser.objects.filter(id=userId).first()
        #scholar = request.POST.get('scholar_name')
        scholar = Scholar.objects.get(id=scholarId)
        if user:
            oldCode = Code.objects.filter(sendTo=user).first()
            if oldCode:
                currentTime = datetime. datetime.now()
                if code == oldCode.code:
                    if timezone.now() <= oldCode.updatedAt + timedelta(minutes=15):
                        #uncertain
                        user.scholarAuth = scholar
                        scholar.belongTo = user
                        scholar.save()
                        oldCode.delete()
                        return UTF8JsonResponse({'errno': 1002, 'msg': "认领学者成功"})
                    else:
                        return UTF8JsonResponse({'errno': 3003, 'msg': "验证码已过期"})
                else:
                    return UTF8JsonResponse({'errno': 3004, 'msg': "验证码不正确"})
            else:
                return UTF8JsonResponse({'errno': 3005, 'msg': "用户没有申请学者认证"})
        else:
            return UTF8JsonResponse({'errno': 3001, 'msg': "用户不存在"})
