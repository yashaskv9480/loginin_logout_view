from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.urls import path
from .models import UserLog

class UserLogInline(admin.TabularInline):
    model = UserLog
    extra = 0
    readonly_fields = ('login_time', 'logout_time')

class CustomUserAdmin(UserAdmin):
    inlines = [UserLogInline]

    def view_logs(self, obj):
        logs_url = reverse('admin:view_user_logs', args=[obj.id])
        return format_html('<a href="{}">View Logs</a>', logs_url)

    view_logs.short_description = 'User Logs'

    list_display = ('username', 'email', 'is_active', 'view_logs')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('view_logs/<int:user_id>/', self.admin_site.admin_view(self.view_user_logs), name='view_user_logs'),
        ]
        return custom_urls + urls

    def view_user_logs(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user_logs = UserLog.objects.filter(user=user)

        context = {
            'user': user,
            'user_logs': user_logs,
        }

        return render(request, 'view_user_logs.html', context)


# @admin.register(UserLog)
# class Userlogadmin(admin.ModelAdmin):
#     list_display = ['action', 'username', 'ip',]
#     list_filter = ['action',]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserLog)


