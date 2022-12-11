import uuid
from django.db import models
from django.utils import timezone


class UserScholar(models.Model):
    scholar = models.CharField(max_length=40)
    scholarName = models.CharField(max_length=150,null=True, blank=True)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    isFollow = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)


class UserArticle(models.Model):
    article = models.ForeignKey("Article", on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)

    isBookmark = models.BooleanField(default=False)
    isDownload = models.BooleanField(default=False)
    
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)

##########################################################################
# 用户给学者发送私信请求 
class UserRequestScholar(models.Model): #等同于request + chatBox
    
    STATUS = (
        (0, '已发送'),
        (1, '通过'),
        (2, '拒绝'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False ,related_name="user")
    scholar = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False,related_name="scholar")
    status = models.IntegerField(choices=STATUS,default=0)
    unread = models.IntegerField(default=0)


    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
