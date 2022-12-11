import uuid
from django.utils import timezone
from django.db import models


class TrendSearch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    keyword = models.CharField(max_length=150,blank=True)
    count = models.IntegerField();
    content = models.TextField(max_length=5000)  

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
