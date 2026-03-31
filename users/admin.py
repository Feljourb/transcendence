from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # هاد السطر كايحدد شنو غايبان في القائمة الرئيسية
    list_display = ('username', 'email', 'location', 'is_staff')
    
    # هاد الجزء هو المهم: كايزيد الحقول ديالك لصفحة التعديل
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('bio', 'location', 'skills', 'avatar')}),
    )
    
    # هاد الجزء لصفحة "إضافة يوزر جديد"
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('bio', 'location', 'skills', 'avatar')}),
    )

admin.site.register(User, CustomUserAdmin)