from django.contrib import admin

from report.models import CrimeReport, PoliceStation
from django.urls import reverse
from django.utils.html import format_html


@admin.register(CrimeReport)
class CrimeReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone_number', 'crime_datetime', 'status', 'action_buttons')
    list_filter = ('status', 'crime_datetime',"report_taken_by_station")
    search_fields = ('title', 'description')
    
    def action_buttons(self, obj):
        return format_html(
            '<div class="action-buttons">'
            '<a href="{}" class="button">Edit</a> '
            '<a href="{}" class="button" style="background-color: #ff4444;">Delete</a>'
            '</div>',
            reverse('admin:report_crimereport_change', args=[obj.pk]),
            reverse('admin:report_crimereport_delete', args=[obj.pk])
        )
    action_buttons.short_description = 'Actions'
    action_buttons.allow_tags = True


# admin.site.register(PoliceStation)


@admin.register(PoliceStation)
class PoliceStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location',"action_buttons")
    list_filter = ('name', 'location')
    search_fields = ('name', 'location')
    
    def action_buttons(self, obj):
        return format_html(
            '<div class="action-buttons">'
            '<a href="{}" class="button">Edit</a> '
            '<a href="{}" class="button" style="background-color: #ff4444;">Delete</a>'
            '</div>',
            reverse('admin:report_policestation_change', args=[obj.pk]),
            reverse('admin:report_policestation_delete', args=[obj.pk])
        )
    action_buttons.short_description = 'Actions'
    action_buttons.allow_tags = True