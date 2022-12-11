import uuid
from django.utils import timezone
from django.db import models

#提问/回答/追问追答
class Question(models.Model):
    CATEGORY = (
        (0, '主问题'),
        (1, '提问'),
        (2, '回复'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=5000)
    scholar = models.CharField(max_length=40)
    #null if is the primary question
    belongToQuestion = models.ForeignKey("Question", on_delete=models.CASCADE, null=True, blank=True)
    category = models.IntegerField(choices=CATEGORY,default=0)
    createdBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
   
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)