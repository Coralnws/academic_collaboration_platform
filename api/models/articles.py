import uuid
from django.utils import timezone
import datetime
from django.db import models
from datetime import date

class Article(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    author = models.ForeignKey("Scholar", on_delete=models.CASCADE, null=False, blank=False)
    citation = models.CharField(max_length=150)

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)