from django.urls import path
from . import views
from .views import  add_Category, add_WeeklyReport, add_annual_budget, add_project_clearance, add_report_achievement, add_report_backlog, add_report_highlights, am_remarks, ceo_am_approve, ceo_aproval_dip, ceoevent, ceoplanapproval, ceoreportapproval, dip_remarks, event_remarks, index,complince_home, location_count, add_Project, monthly_report, plan_remarks, report_remarks, timeframe, update_Activity, update_MonthPlan,update_Project,index1,add_Activity,registerPage,loginPage,logoutUser,index2,add_MonthPlan,index4,add_DIP_Details, update_WeeklyReport, update_component, update_location, update_report, update_timeframe, index6,add_event,update_event, weekly_report
app_name = "myAPP"   


urlpatterns = [
    path('login/', loginPage,name='login'),
    path('logout/', logoutUser,name='logout'),
    path("<int:pk>/", views.home, name="home"),
    path("", views.masterhome, name="masterhome"),


    path('index/', index, name='index'),
    path('add-category/', add_Category, name='add-category'),
    path('add-project/',add_Project,name='add_Project'),
    path('updateProject/<project_id>',update_Project, name='update'),
    
    
    path('dip-detalis/<int:pk>/',add_DIP_Details,name='add_DIP_Details'),
    path('add-activity/<int:pk>',add_Activity,name='add_ActivityMatrix'),
    path('update-activity/<int:pk>',update_Activity,name='update_ActivityMatrix'),
    path('ceo-dip-detalis/<int:pk>/',ceo_aproval_dip,name='ceo_aproval_dip'),
    path('ceo-dip-remark/<int:pk>/', dip_remarks , name='ceo_dip_remark'),


    path('activity-matrix/<int:pk>/', index1, name='index1'),
    path('add-location/<int:pk>/',location_count,name='add_count'),
    path('update-location/<int:pk>/', update_location ,name='update-location'),
    path('add-timeframe/<int:pk>/', timeframe ,name='timeframe'),
    path('update-timeframe/<int:pk>/', update_timeframe ,name='update-timeframe'),
    path('ceo-am/<int:pk>/', ceo_am_approve, name='ceo_am_approve'),
    path('ceo-am-remark/<int:pk>/', am_remarks , name='ceo_am_remark'),
    

    path('monthly-plan/<int:pk>/', index2, name='index2'),
    path('add-monthly-plan/<int:pk>/',add_MonthPlan,name='add_MonthPlan'),
    path('update-monthly-plan/<int:pk>/',update_MonthPlan,name='update_MonthPlan'),
    path('ceo-plan/<int:pk>/', ceoplanapproval, name='ceo_plan_approve'),
    path('ceo-plan-remark/<int:pk>/', plan_remarks , name='ceo_plan_remark'),


    path('event-plan/<int:pk>/', index6, name='index6'),
    path('add-event-plan/<int:pk>/',add_event,name='add_event'),
    path('update-event-plan/<int:pk>/',update_event,name='update_event'),
    path('ceo-event/<int:pk>/', ceoevent , name='ceo_event_approve'),
    path('ceo-event-remark/<int:pk>/', event_remarks , name='ceo_event_remark'),


    path('reporting/<int:pk>/', index4, name='manager-reporting'),
    path('monthly-reporting/<int:pk>/', monthly_report, name='monthly-reporting'),
    path('add-monthly-achievements/<int:pk>/', add_report_achievement, name='add-monthly-achievements'),
    path('add-monthly-highlights/<int:pk>/', add_report_highlights, name='add-monthly-highlights'),
    path('add-monthly-backlog/<int:pk>/', add_report_backlog, name='add-monthly-backlog'),
    path('update-monthly-backlog/<int:pk>/', update_report, name='update-monthly-backlog'),
    path('ceo-report/<int:pk>/', ceoreportapproval , name='ceo_report_approve'),
    path('ceo-report-remark/<int:pk>/', report_remarks , name='ceo_report_remark'),
    path('weekly-report/<int:pk>/', weekly_report, name='weekly-report'),
    path('add-weekly-report/<int:pk>/',add_WeeklyReport,name='add-weekly-report'),
    path('update-weekly-report/<int:pk>/',update_WeeklyReport,name='update-weekly-report'),
    # path('remarks-weekly-report/<int:pk>/',week_remarks,name='remarks-weekly-report'),



    path('complince-home/<int:pk>/', complince_home, name='complince-home'),
    path('add-Monthly-project-clearance-report/<int:pk>/',add_project_clearance,name='add-mpc-report'),





    


    path('update/<int:pk>/',update_component,name='update_component'),

    path('signup/',registerPage, name='signup'),
    path('addAnnualBudget',add_annual_budget,name='add_Annual_Budget'),
    
    
]