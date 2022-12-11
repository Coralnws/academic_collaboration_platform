from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import random

from backend import settings
from api.models import *

#send_smtp(newUser, request, newToken, "Activate Account", "register_email.txt", True)
def send_smtp(user,scholar,request,code,subject, fileName):
    context = {
        'username': user.username,
        'scholar' : scholar.name,
        'code' : code,
        'email': user.email
    }
    print(settings.EMAIL_FROM_USER)
    email = EmailMessage(
        subject,
        render_to_string(fileName, context),
        settings.EMAIL_FROM_USER, # FROM
        [user.email],    #TO
    )

    email.send(fail_silently=False)
    #return JsonResponse({'errno': 1001, 'msg': "邮件已发送"})

def gen_code(length=6):
    str1 = '0123456789'
    rand_str = ''
    for i in range(0, 6):
        rand_str += str1[random.randrange(0, len(str1))]
        print(rand_str)
    return rand_str

def addNotification(user,content):
    notification = Notification(user=user,content=content)
    notification.save()