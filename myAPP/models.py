from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User , Group , AbstractBaseUser


class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE , null=True)
   gender = models.CharField(max_length=6, choices=[('Male','Male'),('Female','Female'),('Others','Others')],null=True, blank=True)
   designation = models.CharField(max_length=30,null=True, blank=True)
   address = models.CharField(max_length=200,null=True, blank=True)
   phone_no = models.IntegerField(null=True, blank=True)
   profile_pic = models.ImageField(upload_to='images/Profile_pics',null=True, blank=True)
   
   def __str__(self):
        return self.user.username


class Project_Category(models.Model):   
 Category_name=models.CharField(max_length=200)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)  
  
 def __str__(self):
        return self.Category_name
# default_user, created = User.objects.get(username='Rajendra_meher')
class Project_DIP(models.Model):   
 project_name=models.CharField(max_length=200)
 category_id = models.ForeignKey("Project_Category", on_delete=models.CASCADE)
 assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
 budget = models.CharField(max_length=200)
 start_date = models.DateField()
 end_date = models.DateField()
 period = models.IntegerField()
 donor_name=models.CharField(max_length=200)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)  
  
 def __str__(self):
        return self.project_name


class TrackingYear(models.Model):
   """
   This will be used as a filter element to
   Filter different compinenets falling in filtered tracking_year
   given a project.
   """
   name =  models.CharField(max_length=200)
   def __str__(self):
        return self.name
class Dip_details(models.Model):
   """
   This is the object for Component, Connected to a project.
   """
   project_id  = models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
   component   = models.CharField(max_length=200)
   tracking_year = models.ForeignKey(TrackingYear ,
                                      blank  =  True,
                                      null   =  True ,
                                      on_delete =   models.CASCADE) #BUDD
   # ^ This will be used to label a component
   # according to the finacial year they fall in-to
   created_at = models.DateTimeField('created at', auto_now_add=True)
   updated_at = models.DateTimeField('updated at', auto_now=True)
   def __str__(self):
         return self.component
   def save(self, *args, **kwargs):
        project_month = self.project_id.start_date.month
        self.created_at = datetime.now()

        if project_month <= self.created_at.month:
            # If the start month is same or after the project month
            tracking_year_name = f"Tracking Year of {self.created_at.year} - {self.created_at.year + 1}"
        else:
            tracking_year_name = f"Tracking Year of {self.created_at.year - 1} - {self.created_at.year }"

        tracking_year, _   = TrackingYear.objects.get_or_create(name=tracking_year_name)
        self.tracking_year = tracking_year

        super().save(*args, **kwargs)

class Dip_Activities(models.Model):
   project_detail_id= models.ForeignKey("DIP_details", on_delete=models.CASCADE)
   activity_name = models.CharField(max_length=200)
   objectives = models.CharField(max_length=200)
   target_participants = models.CharField(max_length=200,null=True)
   target = models.IntegerField(null=True,blank=True)
   coverage = models.CharField(max_length=200,null=True)
   duration = models.CharField(max_length=200,null=True)
   dip_remarks=models.CharField(max_length=200,null=True,blank=True)
   am_remarks=models.CharField(max_length=200,null=True,blank=True)
   is_dip_submited = models.BooleanField(default=False)
   is_dip_approved = models.BooleanField(default=False)
   is_dip_rejected = models.BooleanField(default=False)
   is_am_submited = models.BooleanField(default=False)
   is_am_approved = models.BooleanField(default=False)
   is_am_rejected = models.BooleanField(default=False)     
   created_at = models.DateTimeField('created at', auto_now_add=True)
   updated_at = models.DateTimeField('updated at', auto_now=True) 


   def __str__(self):
        return self.activity_name
   
class Activity_timeframe(models.Model):
   activity_id= models.ForeignKey("Dip_Activities", on_delete=models.CASCADE)   
   start_date = models.DateField()
   tracking_year = models.ForeignKey(TrackingYear ,blank  =  True,null   =  True ,on_delete =   models.CASCADE)
   m1 = models.BooleanField() 
   m2 = models.BooleanField() 
   m3 = models.BooleanField() 
   m4 = models.BooleanField() 
   m5 = models.BooleanField() 
   m6 = models.BooleanField() 
   m7 = models.BooleanField() 
   m8 = models.BooleanField() 
   m9 = models.BooleanField() 
   m10 = models.BooleanField() 
   m11 = models.BooleanField() 
   m12 = models.BooleanField() 
   created_at = models.DateTimeField('created at', auto_now_add=True)
   updated_at = models.DateTimeField('updated at', auto_now=True) 

   def __str__(self):
        return self.activity_id.activity_name
   
   def save(self, *args, **kwargs):
        project_month = self.start_date.month
        self.created_at = datetime.now()

        if project_month <= self.created_at.month:
            tracking_year_name = f"Tracking Year of {self.created_at.year} - {self.created_at.year + 1}"
        else:
            tracking_year_name = f"Tracking Year of {self.created_at.year - 1} - {self.created_at.year }"

        tracking_year, _   = TrackingYear.objects.get_or_create(name=tracking_year_name)
        self.tracking_year = tracking_year

        super().save(*args, **kwargs)


class Activity_location(models.Model):
 activity_id= models.ForeignKey("Dip_Activities", on_delete=models.CASCADE)   
 location_name=models.CharField(max_length=200)
 count= models.IntegerField()
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)  
  
 def __str__(self):
        return self.location_name

class Dip_Process(models.Model):
   project_activity_id= models.ForeignKey("Dip_Activities", on_delete=models.CASCADE)
   process = models.CharField(max_length=200)

class Dip_Indicator(models.Model):
   project_activity_id= models.ForeignKey("Dip_Activities", on_delete=models.CASCADE)
   indicator = models.CharField(max_length=200)

class Dip_expected_out_come(models.Model):
   project_activity_id= models.ForeignKey("Dip_Activities", on_delete=models.CASCADE)
   expected_out_come = models.CharField(max_length=200)

class Dip_mov(models.Model):
   project_activity_id= models.ForeignKey("Dip_Activities", on_delete=models.CASCADE)
   mov = models.CharField(max_length=200)

class Month_Plan(models.Model):  
 month=models.IntegerField()
 year=models.IntegerField()
 activity_id= models.ForeignKey("Dip_Activities", on_delete=models.CASCADE)   
 strategy = models.CharField(max_length=200)
 duration= models.CharField(max_length=200)
 no_Of_Participants=models.CharField(max_length=200)
 location_Of_Activity=models.CharField(max_length=200)
 main_Responsibility=models.CharField(max_length=200)
 supportive_Responsibility=models.CharField(max_length=200)
 result_Expected=models.CharField(max_length=200)
 target=models.IntegerField(null=True,blank=True)
 target_achived=models.IntegerField(null=True,blank=True)
 plan_remarks=models.CharField(max_length=200,null=True,blank=True)
 report_remarks=models.CharField(max_length=200,null=True,blank=True)
 achievements=models.CharField(max_length=200,null=True,blank=True)
 highlights=models.CharField(max_length=200,null=True,blank=True)
 backlog_justification=models.CharField(max_length=200,null=True,blank=True)
 is_plan_submited = models.BooleanField(default=False)
 is_plan_approved = models.BooleanField(default=False)
 is_plan_rejected = models.BooleanField(default=False)
 is_report_submited = models.BooleanField(default=False)
 is_report_approved = models.BooleanField(default=False)
 is_report_rejected = models.BooleanField(default=False) 
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True) 

class Event_Plan(models.Model):
 project_id= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
 event_name=models.CharField(max_length=200)
 start_date= models.DateField()
 end_date= models.DateField()
 venue=models.CharField(max_length=200)
 no_of_participants=models.CharField(max_length=200)
 main_objective=models.CharField(max_length=200)
 key_event=models.CharField(max_length=200)
 total_budget=models.CharField(max_length=100)
 point_person=models.CharField(max_length=200)
 support_persons=models.CharField(max_length=200)
 any_imp_point=models.CharField(max_length=200,null=True)
 remarks=models.CharField(max_length=200,null=True,blank=True)
 is_submited = models.BooleanField(default=False)
 is_approved = models.BooleanField(default=False)
 is_rejected = models.BooleanField(default=False)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True) 
class MonthlyBudget(models.Model):
 project_id= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
 name = models.CharField(max_length=50)
 designation = models.CharField(max_length=50)
 programme = models.CharField(max_length=50)
 month=models.IntegerField()
 year=models.IntegerField()
 budget_head=models.CharField(max_length=200)
 approved_budget=models.IntegerField()
 requsted_budget=models.IntegerField()
 sanctioned_budget=models.IntegerField(null=True,blank=True)
 amount_settled=models.IntegerField(null=True,blank=True)
 variance=models.CharField(max_length=200,null=True,blank=True)
 remarks=models.CharField(max_length=200,null=True,blank=True)
 is_submited = models.BooleanField(default=False)
 is_approved = models.BooleanField(default=False)
 is_rejected = models.BooleanField(default=False)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True) 



class Weekly_Report(models.Model):
 month=models.IntegerField()
 year=models.IntegerField()
 activity_id= models.ForeignKey("Dip_Activities", on_delete=models.CASCADE)  
 unit = models.IntegerField(null=True,blank=True)
 approved_budget = models.IntegerField(null=True,blank=True)
 cumulative_progress = models.CharField(max_length=500,null=True,blank=True)
 cumulative_utilisation = models.CharField(max_length=500,null=True,blank=True)
 remarks=models.CharField(max_length=200,null=True,blank=True)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)

 def __str__(self):
        return self.activity_id.activity_name 

class Week_one_Report(models.Model):
 COLOR_CHOICES =(
    ('1',"Completed"),
    ('2',"In-Progress"),
    ('3',"Not-Started")
    )
 weekly_Report_id = models.ForeignKey("Weekly_Report", on_delete=models.CASCADE)
 report = models.CharField(max_length=500,null=True,blank=True)
 status = models.CharField(max_length= 10,choices=COLOR_CHOICES,null=True,blank=True)
 def __str__(self):
        return self.weekly_Report_id.activity_id.activity_name 
   
class Week_two_Report(models.Model):
 COLOR_CHOICES =(
    ('1',"Completed"),
    ('2',"In-Progress"),
    ('3',"Not-Started")
    )
 weekly_Report_id = models.ForeignKey("Weekly_Report", on_delete=models.CASCADE)
 report = models.CharField(max_length=500,null=True,blank=True)
 status = models.CharField(max_length= 10,choices=COLOR_CHOICES,null=True,blank=True)
 def __str__(self):
        return self.weekly_Report_id.activity_id.activity_name 
 
class Week_three_Report(models.Model):
 COLOR_CHOICES =(
    ('1',"Completed"),
    ('2',"In-Progress"),
    ('3',"Not-Started")
    )
 weekly_Report_id = models.ForeignKey("Weekly_Report", on_delete=models.CASCADE)
 report = models.CharField(max_length=500,null=True,blank=True)
 status = models.CharField(max_length= 10,choices=COLOR_CHOICES,null=True,blank=True)
 def __str__(self):
        return self.weekly_Report_id.activity_id.activity_name 
 
class Week_four_Report(models.Model):
 COLOR_CHOICES =(
    ('1',"Completed"),
    ('2',"In-Progress"),
    ('3',"Not-Started")
    )
 weekly_Report_id = models.ForeignKey("Weekly_Report", on_delete=models.CASCADE)
 report = models.CharField(max_length=500,null=True,blank=True)
 status = models.CharField(max_length= 10,choices=COLOR_CHOICES,null=True,blank=True)
 def __str__(self):
        return self.weekly_Report_id.activity_id.activity_name 
 
class Week_five_Report(models.Model):
 COLOR_CHOICES =(
    ('1',"Completed"),
    ('2',"In-Progress"),
    ('3',"Not-Started")
    )
 weekly_Report_id = models.ForeignKey("Weekly_Report", on_delete=models.CASCADE)
 report = models.CharField(max_length=500,null=True,blank=True)
 status = models.CharField(max_length= 10,choices=COLOR_CHOICES,null=True,blank=True)
 def __str__(self):
        return self.weekly_Report_id.activity_id.activity_name 

class Case_study(models.Model):
   project_id= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
   case_studies = models.FileField(upload_to='documents/case_studies')
   uploaded_at = models.DateTimeField(auto_now_add=True)
   def __str__(self):
        return self.project_id.project_name 

class Monthly_Project_Clearance(models.Model):
 MONTH_CHOICES =(
    ('1',"JANUARY"),
    ('2',"FEBRUARY"),
    ('3',"MARCH"),
    ('4',"APRIL"),
    ('5',"MAY"),
    ('6',"JUNE"),
    ('7',"JULY"),
    ('8',"AUGUST"),
    ('9',"SEPTEMBER"),
    ('10',"OCTOBER"),
    ('11',"NOVEMBER"),
    ('12',"DECEMBER"),
    )
 project_id= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
 reporting_month = models.CharField(max_length=15,choices=MONTH_CHOICES)
 monthly_project_plan = models.BooleanField()
 individual_plan_updated = models.BooleanField()
 individual_worksheet_updated = models.BooleanField()
 monthly_progress_report_updated  = models.BooleanField()
 outstation_report  = models.BooleanField()
 monthly_budget_submited = models.BooleanField()
 settlement_completed = models.BooleanField()
 project_staff_completed_required_project_compliances = models.BooleanField()
 release_Salary_project_staff_recommend = models.BooleanField()
 staff_reason = models.CharField(max_length=500,null=True,blank=True)
 is_submited = models.BooleanField(default=False)
 is_approvedby_hr = models.BooleanField(default=False)
 is_approvedby_ceo = models.BooleanField(default=False)
 is_rejectedby_hr = models.BooleanField(default=False)
 is_rejectedby_ceo = models.BooleanField(default=False)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)

 def get_reporting_month_display(self):
        return dict(self.MONTH_CHOICES)[self.reporting_month]

class Monthly_staff_clearance(models.Model):
 project_id= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
 month=models.IntegerField()
 year=models.IntegerField()
 name_of_staff = models.CharField(max_length=50)
 designation = models.CharField(max_length=50)
 leave_taken_this_month = models.DateField()
 mpr = models.BooleanField()
 planning = models.BooleanField()
 budget = models.BooleanField()
 case_study = models.BooleanField()
 outstation_report = models.BooleanField()
 event_report = models.BooleanField()
 settlement_completed = models.BooleanField()
 any_other = models.CharField(max_length=300,null=True,blank=True)
 is_submited = models.BooleanField(default=False)
 is_approvedby_hr = models.BooleanField(default=False)
 is_approvedby_ceo = models.BooleanField(default=False)
 is_rejectedby_hr = models.BooleanField(default=False)
 is_rejectedby_ceo = models.BooleanField(default=False)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)

class Leave_Statement(models.Model):
 project_id= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
 name_of_staff = models.CharField(max_length=50)
 designation = models.CharField(max_length=50)
 date_of_joining = models.DateField()
 remarks = models.CharField(max_length=100,null=True, blank=True)
 total_leaves_allowed = models.IntegerField()
 m1_leave = models.IntegerField(default=0, blank=True)
 m2_leave = models.IntegerField(default=0, blank=True)
 m3_leave = models.IntegerField(default=0, blank=True)
 m4_leave = models.IntegerField(default=0, blank=True)
 m5_leave = models.IntegerField(default=0, blank=True)
 m6_leave = models.IntegerField(default=0, blank=True)
 m7_leave = models.IntegerField(default=0, blank=True)
 m8_leave = models.IntegerField(default=0, blank=True)
 m9_leave = models.IntegerField(default=0, blank=True)
 m10_leave = models.IntegerField(default=0, blank=True)
 m11_leave = models.IntegerField(default=0, blank=True)
 m12_leave = models.IntegerField(default=0,blank=True)
 total_leaves_remaining = models.IntegerField()
 is_submited = models.BooleanField(default=False)
 is_approvedby_hr = models.BooleanField(default=False)
 is_approvedby_ceo = models.BooleanField(default=False)
 is_rejectedby_hr = models.BooleanField(default=False)
 is_rejectedby_ceo = models.BooleanField(default=False)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)

 def __str__(self):
        return self.name_of_staff


class Leave_Application(models.Model):
 LEAVE_CHOICES =(
    ('1',"Privilege"),
    ('2',"Sick")
    )
 project_id= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
 name_of_staff = models.CharField(max_length=50)
 designation = models.CharField(max_length=50)
 date = models.DateField(auto_now_add=True)
 leave_requested_from = models.DateField()
 leave_requested_to = models.DateField()
 type_of_leave = models.CharField(max_length=10,choices=LEAVE_CHOICES)
 leave_balance_till_to_date = models.IntegerField()
 address =  models.CharField(max_length=50)
 phone_no =  models.CharField(max_length=15)
 is_submited = models.BooleanField(default=False)
 is_approved = models.BooleanField(default=False)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)

 def get_display(self):
        return dict(self.LEAVE_CHOICES)[self.type_of_leave]
   

class Appraisal(models.Model):
 CHOICES =(
    ('1',"Annually"),
    ('2',"Half yearly")
    )
 project_id= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
 name_of_staff = models.CharField(max_length=50)
 designation = models.CharField(max_length=50)
 appraisal_period_start_date = models.DateField()
 appraisal_period_end_date = models.DateField()
 type_of_appraisal = models.CharField(max_length=10,choices=CHOICES)
 name_of_the_appraisal_authority =  models.CharField(max_length=50)
 appraisal_authority_designation =  models.CharField(max_length=15)
 dedication = models.IntegerField(default=0)
 performance = models.IntegerField(default=0)
 cooperation = models.IntegerField(default=0)
 initiative = models.IntegerField(default=0)
 communication = models.IntegerField(default=0)
 teamwork = models.IntegerField(default=0)
 documentation_reporting = models.IntegerField(default=0)
 problem_solving= models.IntegerField(default=0)
 personality = models.IntegerField(default=0)
 overall_Rating = models.IntegerField(default=0)
 recommendation =  models.CharField(max_length=100,blank=True,null=True)
 is_submited = models.BooleanField(default=False)
 is_approved = models.BooleanField(default=False)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)

 def get_display(self):
        return dict(self.CHOICES)[self.type_of_appraisal]


class Asset(models.Model):
 CHOICES =(
    ('1',"Good"),
    ('2',"Poor")
    )
 project_id= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
 name_of_asset = models.CharField(max_length=50)
 asset_id_no = models.CharField(max_length=50)
 status = models.CharField(max_length=10,choices=CHOICES)
 unit = models.IntegerField()
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)

 def get_display(self):
        return dict(self.CHOICES)[self.status]


class Clearance_Admin(models.Model):
 project_id= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
 name = models.CharField(max_length=50)
 designation = models.CharField(max_length=50)
 last_date = models.DateField()
 location =  models.CharField(max_length=100)
 resignation =  models.CharField(max_length=100)
 programme_remarks = models.CharField(max_length=100,blank=True,null=True)
 programme_signature = models.ImageField(upload_to='images/clearance_admin_signatures',blank=True,null=True)
 finance_remarks = models.CharField(max_length=100,blank=True,null=True)
 finance_signature = models.ImageField(upload_to='images/clearance_admin_signatures',blank=True,null=True)
 administration_remarks = models.CharField(max_length=100,blank=True,null=True)
 administration_signature = models.ImageField(upload_to='images/clearance_admin_signatures',blank=True,null=True)
 office_secretary_remarks = models.CharField(max_length=100,blank=True,null=True)
 office_secretary_signature = models.ImageField(upload_to='images/clearance_admin_signatures',blank=True,null=True)
 misc_remarks = models.CharField(max_length=100,blank=True,null=True)
 misc_signature = models.ImageField(upload_to='images/clearance_admin_signatures',blank=True,null=True)
 is_submited = models.BooleanField(default=False)
 is_approved = models.BooleanField(default=False)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)


class Clearance_Programme(models.Model):
 project_id= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
 name = models.CharField(max_length=50)
 designation = models.CharField(max_length=50)
 location =  models.CharField(max_length=100)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)

class Clearance_Programme_key_activities(models.Model):
 cp_id= models.ForeignKey("Clearance_Programme", on_delete=models.CASCADE)
 activity_name = models.CharField(max_length=50)
 current_status = models.CharField(max_length=100)
 way_forward =  models.CharField(max_length=100)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)

class OutStation(models.Model):
 project_id= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
 name = models.CharField(max_length=50)
 designation = models.CharField(max_length=50)
 period_of_travel_from = models.DateField()
 period_of_travel_to = models.DateField()
 purpose =  models.CharField(max_length=100)
 place_to_be_visited =  models.CharField(max_length=100)
 tentative_programme_during_visit = models.CharField(max_length=100,blank=True,null=True)
 estimated_travel_cost = models.IntegerField()
 means_of_transportation = models.CharField(max_length=100,blank=True,null=True)
 remarks = models.CharField(max_length=100,blank=True,null=True)
 date_of_submission = models.DateField(blank=True,null=True)
 ceo_note = models.CharField(max_length=100,blank=True,null=True)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)





