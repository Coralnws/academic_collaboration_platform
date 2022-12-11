import uuid
from django.utils import timezone
from django.db import models

class Message(models.Model):
    SENTFROM = (
        (0, '用户'),
        (1, '对方'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=5000)
    # 和 UserRequestScholar 连续，来决定是否有同意私信
    userRequestScholar = models.ForeignKey("UserRequestScholar", on_delete=models.CASCADE, null=False, blank=False)
    sentBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=True, blank=False)
    sentFrom = models.IntegerField(choices=SENTFROM, default=0) # 该 message 是谁给谁发的
    seen = models.BooleanField(default=False)

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)