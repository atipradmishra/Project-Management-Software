from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportMixin
from import_export.admin import ImportExportModelAdmin
from .resources import ProjectResource, UserResource

class CustomUserAdmin(ImportExportMixin, UserAdmin):
    resource_class = UserResource

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Project_DIP)
class CustomProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource

class ProjectAdmin(admin.ModelAdmin):
  date_hierarchy = 'created_at'
  list_filter = ('period','project_name')
  search_fields = ['project_name','period']
# admin.site.register(Project_DIP, ProjectAdmin)
admin.site.register(Profile)
admin.site.register(Activity_timeframe)
admin.site.register(Dip_details)
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

  
   








 




