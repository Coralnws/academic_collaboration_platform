import uuid
from django.utils import timezone
from django.db import models


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150,blank=True)
    content = models.TextField(max_length=5000)  

    createdBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)
    article = models.CharField(max_length=40,null=True,blank=True)
    review = models.ForeignKey("Review", on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='review_under_review')

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
