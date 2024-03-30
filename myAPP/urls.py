from django.urls import path
from .views import Projects_list, add_Activity, add_Category, add_DIP_Details, add_MonthPlan, add_Project, add_WeeklyReport, add_admin_clearance, add_appraisal, add_asset, add_budget_request, add_event, add_leave_application, add_leaves, add_leaves_monthly, add_leaving_station, add_msc, add_programme_clearance, add_project_clearance, add_report_achievement, add_report_backlog, add_report_highlights, add_user, am_remarks, appraisals, assets, budget_requests, category_list, ceo_am_approve, ceo_aproval_dip, ceo_profile, ceoevent, ceoplanapproval, ceoreportapproval, clearance_admin, clearance_programme, complince_home, create_weekly_report, dip_remarks, display_docs, download_document, edit_budget_request, edit_leave_application, edit_project_clearance, event_remarks, export_to_excel, governance_home, home, hrhome, index1, index2, index4, index6, leave_application, leaves, leaving_station, location_count, loginPage, logoutUser, masterhome, monthly_report, msc, plan_remarks, project_clearance, report_remarks, timeframe, update_Activity, update_Category, update_MonthPlan, update_Project, update_WeeklyReport, update_asset, update_component, update_event, update_location, update_msc, update_report, update_timeframe, update_weekly_report, upload_document, user_profile, userhome, users_list, weekly_report 
from django.conf import settings
from django.conf.urls.static import static
app_name = "myAPP"   


urlpatterns = [
    path('login/', loginPage,name='login'),
    path('logout/', logoutUser,name='logout'),
    path("dashboard/<int:pk>/", userhome, name="pm-home"),
    path("hr-dashboard", hrhome, name="hr-home"),
    path("", masterhome, name="masterhome"),

    path("planning-home/<int:pk>/", home, name="home"),
    path('add-user/', add_user, name='add-user'),
    path('add-category/', add_Category, name='add-category'),
    path('edit-category/<int:pk>', update_Category, name='edit-category'),
    path('add-project/',add_Project,name='add_Project'),
    path('updateProject/<int:pk>',update_Project, name='update-project'),
    path('project-list/',Projects_list,name='Project-list'),
    path('category-list/',category_list,name='Category-list'),
    path('users-list/',users_list,name='user-list'),
    
    path("profile/<int:pk>/", user_profile , name="profile"),
    path("profile/", ceo_profile , name="ceo_profile"),
    
    path('dip-detalis/<int:pk>/',add_DIP_Details,name='add_DIP_Details'),
    path('dip-download/<int:pk>/',export_to_excel,name='dip-download'),
    path('update/<int:pk>/',update_component,name='update_component'),
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


    path('budget-requests-list/<int:pk>/', budget_requests , name='budget_requests'),
    path('add-budget-request/<int:pk>/', add_budget_request , name='add_budget_request'),
    path('edit-budget-request/<int:pk>/', edit_budget_request , name='edit_budget_request'),


    path('reporting-home/<int:pk>/', index4, name='manager-reporting'),
    path('monthly-reporting/<int:pk>/', monthly_report, name='monthly-reporting'),
    path('add-monthly-achievements/<int:pk>/', add_report_achievement, name='add-monthly-achievements'),
    path('add-monthly-highlights/<int:pk>/', add_report_highlights, name='add-monthly-highlights'),
    path('add-monthly-backlog/<int:pk>/', add_report_backlog, name='add-monthly-backlog'),
    path('update-monthly-backlog/<int:pk>/', update_report, name='update-monthly-report'),
    path('ceo-report/<int:pk>/', ceoreportapproval , name='ceo_report_approve'),
    path('ceo-report-remark/<int:pk>/', report_remarks , name='ceo_report_remark'),
    path('weekly-report/<int:pk>/', weekly_report, name='weekly-report'),
    path('add-weekly-report/<int:pk>/',add_WeeklyReport,name='add-weekly-report'),
    path('update-weekly-report/<int:pk>/',update_WeeklyReport,name='update-weekly-report'),
    path('create-weekly-report/<int:pk>/', create_weekly_report, name='create_weekly_report'),
    path('edit-weekly-report/<int:pk>/', update_weekly_report, name='update_weekly_report'),
    path('case-studies/<int:pk>/',upload_document,name='case-studies'),
    path('view/<int:document_id>/', display_docs, name='view_document'),
    path('download/<int:document_id>/', download_document, name='download_document'),



    path('complince-home/<int:pk>/', complince_home, name='complince-home'),
    path('add-Monthly-project-clearance-report/<int:pk>/',add_project_clearance,name='add-mpc-report'),
    path('edit-Monthly-project-clearance-report/<int:pk>/',edit_project_clearance,name='edit-mpc-report'),
    path('Monthly-project-clearance-report/<int:pk>/',project_clearance,name='mpc-report'),
    path('Leave-Statement-Staff-Clearance/<int:pk>/', leaves ,name='leaves'),
    path('add-leave-statement/<int:pk>/',add_leaves,name='add-leave'),
    path('add-leave-monthly/<int:pk>/',add_leaves_monthly,name='add-leave-monthly'),
    path('monthly-staff-clearance/<int:pk>/', msc ,name='msc'),
    path('add-monthly-staff-clearance/<int:pk>/',add_msc,name='add-msc'),
    path('edit-monthly-staff-clearance/<int:pk>/',update_msc,name='edit-msc'),


    path('governance-home/<int:pk>/',governance_home,name='governance-home'),
    path('leave-application/<int:pk>/',leave_application,name='leave-application'),
    path('add-leave-application/<int:pk>/',add_leave_application,name='add-leave-application'),
    path('edit-leave-application/<int:pk>/',edit_leave_application,name='edit-leave-application'),
    path('appraisal-list/<int:pk>/',appraisals,name='appraisal'),
    path('add-appraisal/<int:pk>/',add_appraisal,name='add-appraisal'),
    path('assets-list/<int:pk>/',assets,name='assets'),
    path('add-asset/<int:pk>/',add_asset,name='add-asset'),
    path('edit-asset/<int:pk>/',update_asset,name='update-asset'),
    path('clearance-admin/<int:pk>/',clearance_admin,name='clearance-admin'),
    path('add-admin-clearance/<int:pk>/',add_admin_clearance,name='add-admin-clearance'),
    path('clearance-programme/<int:pk>/',clearance_programme,name='clearance-programme'),
    path('add-programme-clearance/<int:pk>/',add_programme_clearance,name='add-programme-clearance'),
    path('leaving-station/<int:pk>/',leaving_station,name='leaving-station'),
    path('add-leaving-station/<int:pk>/',add_leaving_station,name='add-leaving-station'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)