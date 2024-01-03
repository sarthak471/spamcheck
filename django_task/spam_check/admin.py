from django.contrib import admin
from .models import Registor_Contact,Registor_User
# Register your models here.

@admin.register(Registor_User)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','Name','Password','Phone_no','Email']

@admin.register(Registor_Contact)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','User_id','Contact_no','Name','spam']