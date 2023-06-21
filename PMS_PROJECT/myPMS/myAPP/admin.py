from django.contrib import admin
from .models import Activity_location, Activity_timeframe, Dip_Activities, Dip_Indicator, Dip_Process, Dip_expected_out_come, Dip_mov, Event_Plan, Monthly_Project_Clearance, Project_Category, Project_DIP,Month_Plan,Dip_details, Week_five_Report, Week_four_Report, Week_one_Report, Week_three_Report, Week_two_Report, Weekly_Report
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
admin.site.register(Monthly_Project_Clearance)

  
   








 




