import uuid
from django.utils import timezone
from django.db import models

class Notification(models.Model):
    TYPE = (
        (0, '无'),
        (1, '关注'),
        (2, '申诉接受'),
        (3, '申诉驳回'),
        (4, '门户认领成功'),
        (5, '门户解除'),
        (6, '评论论文'),
        (7, '回复评论'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=5000)
    
    belongTo = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    #type 1,6,7
    userId = models.CharField(max_length=40,null=True,blank=True)
    userName = models.CharField(max_length=150,null=True,blank=True)
    #type 1,2,3,4,5
    scholarId = models.CharField(max_length=40,null=True,blank=True)
    scholarName = models.CharField(max_length=150,null=True,blank=True)
    #type 6,7
    paperId = models.CharField(max_length=40,null=True,blank=True)
    paperName = models.CharField(max_length=150,null=True,blank=True)
    #type 7
    reviewId = models.CharField(max_length=40,null=True,blank=True)
    type = models.IntegerField(choices=TYPE,default=0)
    
    seen = models.BooleanField(default=False)

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)