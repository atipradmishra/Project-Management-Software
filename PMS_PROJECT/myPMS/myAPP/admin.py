from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportMixin
from import_export.admin import ImportExportModelAdmin
from .resources import ProfileResource, ProjectResource, UserResource

class CustomUserAdmin(ImportExportMixin, UserAdmin):
    resource_class = UserResource

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class CustomProfileAdmin(ImportExportModelAdmin):
    resource_class = ProfileResource

@admin.register(Project_DIP)
class CustomProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource

class ProjectAdmin(admin.ModelAdmin):
  date_hierarchy = 'created_at'
  list_filter = ('period','project_name')
  search_fields = ['project_name','period']
# admin.site.register(Project_DIP, ProjectAdmin)
# admin.site.register(Profile)
  
class Dip_detailsAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'component','tracking_year', 'created_at', 'updated_at')
    list_filter = ('project_id', 'created_at', 'updated_at')
    search_fields = ('project_id__name', 'component')

    fieldsets = (
        (None, {
            'fields': ('project_id', 'component','tracking_year', )
        }),
        ('Date Information', {
            'fields': ('created_at','created',  'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('project_id', 'component')
        return self.readonly_fields

admin.site.register(Dip_details, Dip_detailsAdmin)
admin.site.register(Activity_timeframe)
admin.site.register(Project_Category)
admin.site.register(Dip_Activities)
admin.site.register(Dip_Process)
admin.site.register(Dip_Indicator)
admin.site.register(Dip_expected_out_come)
admin.site.register(Dip_mov)
admin.site.register(Activity_location)
admin.site.register(Event_Plan)
admin.site.register(Month_Plan)
admin.site.register(Weekly_Report)
admin.site.register(Week_one_Report)
admin.site.register(Week_two_Report)
admin.site.register(Week_three_Report)
admin.site.register(Week_four_Report)
admin.site.register(Week_five_Report)
admin.site.register(Case_study)
admin.site.register(Monthly_Project_Clearance)
admin.site.register(Monthly_staff_clearance)
admin.site.register(Leave_Statement)
admin.site.register(Leave_Application)
admin.site.register(Appraisal)
admin.site.register(Asset)
admin.site.register(Clearance_Admin)
admin.site.register(Clearance_Programme)
admin.site.register(Clearance_Programme_key_activities)
admin.site.register(OutStation)
admin.site.register(MonthlyBudget)

  
   








 




