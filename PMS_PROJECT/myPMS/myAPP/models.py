from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User , Group


class Project_Category(models.Model):   
 Category_name=models.CharField(max_length=200)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)  
  
 def __str__(self):
        return self.Category_name

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


class Dip_details(models.Model):
 project_id= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
 component = models.CharField(max_length=200)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)
 def __str__(self):
        return self.component  

class Dip_Activities(models.Model):
   project_detail_id= models.ForeignKey("DIP_details", on_delete=models.CASCADE)
   activity_name = models.CharField(max_length=200)
   objectives = models.CharField(max_length=200)
   target_participants = models.CharField(max_length=200,null=True)
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


class Weekly_Report(models.Model):
 month=models.IntegerField()
 year=models.IntegerField()
 activity_id= models.ForeignKey("Dip_Activities", on_delete=models.CASCADE)  
 unit = models.IntegerField(null=True,blank=True)
 approved_budget = models.IntegerField(null=True,blank=True)
 w1 = models.CharField(max_length=500,null=True,blank=True)
 w2 = models.CharField(max_length=500,null=True,blank=True)
 w3 = models.CharField(max_length=500,null=True,blank=True)
 w4 = models.CharField(max_length=500,null=True,blank=True)
 w5 = models.CharField(max_length=500,null=True,blank=True)
 cumulative_progress = models.CharField(max_length=500,null=True,blank=True)
 cumulative_utilisation = models.CharField(max_length=500,null=True,blank=True)
 remarks=models.CharField(max_length=200,null=True,blank=True)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)

 def __str__(self):
        return self.activity_id.activity_name 

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
 staff_reason = models.CharField(max_length=500,null=True)
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)

# class Monthly_staff_clearance(models.Model):
#  project_id= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
#  name_of_staff = models.CharField(max_length=50)
#  designation = models.CharField(max_length=50)
#  leave_taken_this_month = models.DateField()
#  mpr = models.BooleanField()
#  planning = models.BooleanField()
#  budget = models.BooleanField()
#  settelement_status = models.BooleanField()
#  settlement_completed = models.BooleanField()
#  created_at = models.DateTimeField('created at', auto_now_add=True)
#  updated_at = models.DateTimeField('updated at', auto_now=True)








class Week_one_Report(models.Model):
 COLOR_CHOICES =(
    ('1',"Completed"),
    ('2',"In-PROGRESS"),
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
    ('2',"In-PROGRESS"),
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
    ('2',"In-PROGRESS"),
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
    ('2',"In-PROGRESS"),
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
    ('2',"In-PROGRESS"),
    ('3',"Not-Started")
    )
 weekly_Report_id = models.ForeignKey("Weekly_Report", on_delete=models.CASCADE)
 report = models.CharField(max_length=500,null=True,blank=True)
 status = models.CharField(max_length= 10,choices=COLOR_CHOICES,null=True,blank=True)
 def __str__(self):
        return self.weekly_Report_id.activity_id.activity_name 
 
class Annual_budget(models.Model):
 name_of_organization=models.CharField(max_length=200)   
 project_number= models.ForeignKey("Project_DIP", on_delete=models.CASCADE)
 period = models.CharField(max_length=200)
 date_of_budget = models.DateField()
 local_currency = models.CharField(max_length=100)
 exchange_rate = models.CharField(max_length=100)
 date_approved = models.DateField()
 created_at = models.DateTimeField('created at', auto_now_add=True)
 updated_at = models.DateTimeField('updated at', auto_now=True)  
  
 def __str__(self):
        return self.name_of_organization
 

class MonthlyBudget(models.Model):
   exp_code=models.IntegerField()
   name=models.CharField(max_length=200)
   designation=models.CharField(max_length=200)
   programme=models.CharField(max_length=200)
   month=models.CharField(max_length=200)
   head_expenditure=models.CharField(max_length=200)
   amount_requested_previous_month=models.IntegerField()
   amount_requested_current_month=models.IntegerField()
   amount_sanctioned=models.IntegerField()
   created_at = models.DateTimeField('created at', auto_now_add=True)
   updated_at = models.DateTimeField('updated at',auto_now=True)



 
   
