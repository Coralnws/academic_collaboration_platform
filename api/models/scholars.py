import uuid
from django.utils import timezone
import datetime
from django.db import models
from datetime import date

class Scholar(models.Model):
    GENDER = (
        ('O', 'Prefer Not to Say'),
        ('M', 'Male'),
        ('F', 'Female'),
    )


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER, default=GENDER[0][0])
    dob = models.DateField(default=datetime.date(2000, 1, 1))

    description = models.TextField(max_length=5000)
    current_position = models.TextField(max_length=5000)
    #img = models.ImageField(upload_to="uploads/movies", blank=True)
    #thumbnail = models.ImageField(upload_to="uploads/movies", blank=True)
    currentInstitute = models.ForeignKey("Institute", on_delete=models.CASCADE, null=False, blank=False)
    academicField = models.ForeignKey("AcademicField", on_delete=models.CASCADE, null=False, blank=False)
    #academicField = models.CharField(max_length=150)
    
    #after authentication
    belongTo = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=True, blank=True,related_name="authenticateUser")
    authentication_time = models.DateTimeField(null=True, blank=True)

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)