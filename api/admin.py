from django.contrib import admin
from .models import *
# Register your models here.

class UserAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'username','real_name' ,'email')

class ScholarsAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'name','email')


class CodeAdminConfig(admin.ModelAdmin):
    list_display = ('id', 'code','sendTo')

class InstituteAdminConfig(admin.ModelAdmin):
    list_display = ('id','name')

class FieldAdminConfig(admin.ModelAdmin):
    list_display = ('id','title')

admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Scholar, ScholarsAdminConfig)
admin.site.register(Code, CodeAdminConfig)
admin.site.register(Institute, InstituteAdminConfig)
admin.site.register(AcademicField, FieldAdminConfig)
admin.site.register(UserScholar)
admin.site.register(UserRequestScholar)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(Review)
