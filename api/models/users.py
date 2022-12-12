import uuid
from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):

    # Method for creating normal user
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        newUser = self.model(email=email, username=username, **other_fields)
        newUser.set_password(password)
        newUser.save()
        return newUser

    # Method for creating superuser
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff = True."))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser = True."))

        return self.create_user(email, username, password, **other_fields)

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):

    GENDER = (
        ('O', 'Prefer Not to Say'),
        ('M', 'Male'),
        ('F', 'Female'),
    )

    CATEGORY = (
        (1, '普通用户'),
        (2, '学者'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    real_name = models.CharField(max_length=150,blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, default = "A bio hasn't been added yet.")
    is_staff = models.BooleanField(default=False)
    # activated at email validation only, not at registration.
    is_active = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=GENDER, default=GENDER[0][0])
    dob = models.DateField(default=datetime.date(2000, 1, 1))
    profile = models.ImageField(upload_to="uploads/users", blank=True)
    thumbnail = models.ImageField(upload_to="uploads/users", blank=True)
    identity = models.IntegerField(choices=CATEGORY,default=1)
    scholarAuth = models.CharField(max_length=40 ,blank=True,null=True)

    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(default=timezone.now)
    banComment = models.BooleanField(default=False)
    banDuration = models.DateTimeField(blank=True,null=True,default=None)

    objects = CustomUserManager()

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    # class Meta:
    #     app_label = 'api'

    def __str__(self):
        return f'{self.username} ({self.id})'

    def has_perm(self, perm, obj=None):
        """
        A method used to check if the user has permission
        """
        return True

    def tokens(self):
        """
        A method used to get the token of user
        """
        return get_tokens(self)
