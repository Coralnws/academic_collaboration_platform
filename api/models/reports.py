import uuid
from django.db import models
from django.utils import timezone

#申诉
class Report(models.Model):
    CATEGORY = (
        (0, '-'),
        (1, '学者申诉'),
        (2, '学术成果申诉'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=5000)
    reportArticle = models.ForeignKey("Article", on_delete=models.CASCADE, null=True, blank=True)
    reportScholar = models.ForeignKey("Scholar", on_delete=models.CASCADE, null=True, blank=True)
    category = models.IntegerField(choices=CATEGORY,default=0)
    result = models.BooleanField(default=False)
    createdBy = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=False, blank=False)

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)