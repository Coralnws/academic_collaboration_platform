import uuid
from django.utils import timezone
import datetime
from django.db import models
from datetime import date

class Code(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=6)
    sendTo = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=True, blank=True)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)