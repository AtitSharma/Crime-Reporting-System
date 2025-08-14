from django.contrib import admin

from user_management.models import User
# admin.site.register(User)
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name',"email", 'action_buttons')
    list_filter = ('email',)
    search_fields = ('email',)
    
    def action_buttons(self, obj):
        return format_html(
            '<div class="action-buttons">'
            '<a href="{}" class="button">Edit</a> '
            '<a href="{}" class="button" style="background-color: #ff4444;">Delete</a>'
            '</div>',
            reverse('admin:user_management_user_change', args=[obj.pk]),
            reverse('admin:user_management_user_delete', args=[obj.pk])
        )
    action_buttons.short_description = 'Actions'
    action_buttons.allow_tags = True