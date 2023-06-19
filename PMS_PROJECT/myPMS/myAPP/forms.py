from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Activity_location, Activity_timeframe, Dip_Activities, Dip_Indicator, Dip_Process, Dip_expected_out_come, Dip_mov, Monthly_Project_Clearance, Project_Category, Project_DIP,Month_Plan,Dip_details,Event_Plan, Week_five_Report, Week_four_Report, Week_one_Report, Week_three_Report, Week_two_Report, Weekly_Report
from django.forms import ModelForm


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2' ]

class CategoryForm(ModelForm):
     class Meta:
        model = Project_Category
        exclude = () 
        widgets ={ 
        'Category_name': forms.TextInput(attrs={'class':'form-control','placeholder':"Category Name.."}),
     }


class ProjectForm(forms.ModelForm):
    
    assigned_to = forms.ModelChoiceField(queryset=User.objects.exclude(is_superuser = True))

    class Meta:
        model = Project_DIP
        fields =['project_name','start_date','end_date','assigned_to','donor_name','category_id','budget']
        widgets = {
        'period' : forms.HiddenInput(),
        'project_name': forms.TextInput(attrs={'class':'form-control','placeholder' :"Project name...."}),
        'start_date': forms.TextInput(attrs={'type' : 'date'}),
        'end_date': forms.TextInput(attrs={'type' : 'date'}),
        'assigned_to' : forms.Select(choices=['test']),
        'donor_name' : forms.TextInput(attrs={'class':'form-control','placeholder' :"Donor name...."}),
        'budget' : forms.TextInput(attrs={'class':'form-control'}),
        }        

class DipComponentForm(ModelForm):
     class Meta:
        model = Dip_details
        fields = ['component']
        widgets ={ 
        'component': forms.TextInput(attrs={'id':"input1" ,'onkeyup':"capitalizeText('input1')",'class':'form-control','placeholder':"Add Component",'style':'width: 100%;padding: 12px;border: 1px solid #ccc;border-radius: 4px;resize: vertical;'}),
     }
        
        
class LocationCountForm(ModelForm):
     class Meta:
        model = Activity_location
        fields = ['location_name','count']
        widgets ={ 
        'count': forms.TextInput(attrs={'placeholder':"Add Location Count",'style':'float: left; float: left; width: 100%;padding: 12px;border: 1px solid #ccc;border-radius: 4px;resize: vertical;'}),
        'location_name': forms.TextInput(attrs={'id':"input1" ,'onkeyup':"capitalizeText('input1')",'placeholder':"Location Name....",'style':'width: 100%;padding: 12px;border: 1px solid #ccc;border-radius: 4px;resize: vertical;'}),
     }

class DipActivityForm(ModelForm):
     class Meta:
        model = Dip_Activities
        fields = ['activity_name','objectives','target_participants','coverage','duration']
        widgets ={ 
        'activity_name': forms.TextInput(attrs={'class':'form-control'}),
        'objectives': forms.TextInput(attrs={'class':'form-control'}), 
        'target_participants': forms.TextInput(attrs={'class':'form-control'}),
        'coverage': forms.TextInput(attrs={'class':'form-control'}),
        'duration': forms.TextInput(attrs={'class':'form-control'}),
     }
     
class TimeFrameForm(forms.ModelForm):
    class Meta:
        model = Activity_timeframe
        fields = ['m1','m2','m3','m4','m5','m6','m7','m8','m9','m10','m11','m12']


class DipProcessForm(ModelForm):
     class Meta:
        model = Dip_Process
        exclude = () 
        widgets ={ 
        'process': forms.TextInput(attrs={'class':'form-control'}), 
     }

class DipIndicatorForm(ModelForm):
     class Meta:
        model = Dip_Indicator
        exclude = () 
        widgets ={ 
        'indicator': forms.TextInput(attrs={'class':'form-control'}), 
     }

class DipOutcomeForm(ModelForm):
     class Meta:
        model = Dip_expected_out_come
        exclude = () 
        widgets ={ 
        'expected_out_come': forms.TextInput(attrs={'class':'form-control'}), 
     }

class DipMovForm(ModelForm):
     class Meta:
        model = Dip_mov
        exclude = () 
        widgets ={ 
        'mov': forms.TextInput(attrs={'class':'form-control'}), 
     }
        
class ActivityAproveForm(ModelForm):
     class Meta:
        model = Dip_Activities
        fields = ['is_dip_submited']

class CeoAproveForm(ModelForm):
     class Meta:
        model = Dip_Activities
        fields = ['is_dip_approved']

class ActivityMatrixAproveForm(ModelForm):
     class Meta:
        model = Dip_Activities
        fields = ['is_am_submited']

class ActivityMatrixCeoForm(ModelForm):
     class Meta:
        model = Dip_Activities
        fields = ['is_am_approved']

class MonthlyPlanAproveForm(ModelForm):
     class Meta:
        model = Month_Plan
        fields = ['is_plan_approved']

class EventPlanAproveForm(ModelForm):
     class Meta:
        model = Event_Plan
        fields = ['is_submited']

class ReportAproveForm(ModelForm):
     class Meta:
        model = Month_Plan
        fields = ['is_report_approved']

class EventRemarkForm(ModelForm):
     class Meta:
        model = Event_Plan
        fields = ['remarks']
        widgets ={
        'remarks' : forms.TextInput(attrs={'null' : 'True','id':"input1" ,'onkeyup':"capitalizeText('input1')"})
        }

class PlanRemarkForm(ModelForm):
     class Meta:
        model = Month_Plan
        fields = ['plan_remarks']
        widgets ={
        'plan_remarks' : forms.TextInput(attrs={'null' : 'True','id':"input1" ,'onkeyup':"capitalizeText('input1')"})
        }

class ReportRemarkForm(ModelForm):
     class Meta:
        model = Month_Plan
        fields = ['report_remarks']
        widgets ={
        'report_remarks' : forms.TextInput(attrs={'null' : 'True','id':"input1" ,'onkeyup':"capitalizeText('input1')"})
        }

class AmRemarkForm(ModelForm):
     class Meta:
        model = Dip_Activities
        fields = ['am_remarks']
        widgets ={
        'am_remarks' : forms.TextInput(attrs={'null' : 'True','id':"input1" ,'onkeyup':"capitalizeText('input1')"})
        }

class DipRemarkForm(ModelForm):
     class Meta:
        model = Dip_Activities
        fields = ['dip_remarks']
        widgets ={
        'dip_remarks' : forms.TextInput(attrs={'null' : 'True','id':"input1" ,'onkeyup':"capitalizeText('input1')"})
        }


class MonthlyachievementForm(ModelForm):
     class Meta:
        model = Month_Plan
        fields = ['achievements']
        widgets ={
        'achievements' : forms.TextInput(attrs={'null' : 'True','id':"input1" ,'onkeyup':"capitalizeText('input1')"})
        }

class MonthlyhighlightForm(ModelForm):
     class Meta:
        model = Month_Plan
        fields = ['highlights']
        widgets ={
        'highlights' : forms.TextInput(attrs={'null' : 'True','id':"input1" ,'onkeyup':"capitalizeText('input1')"})
        }

class MonthlybacklogForm(ModelForm):
     class Meta:
        model = Month_Plan
        fields = ['backlog_justification']
        widgets ={
        'backlog_justification' : forms.TextInput(attrs={'null' : 'True','id':"input1" ,'onkeyup':"capitalizeText('input1')"})
        }

class MonthlyReportUpdateForm(ModelForm):
     class Meta:
        model = Month_Plan
        fields = ['achievements','highlights','backlog_justification']
        widgets ={
        'achievements' : forms.TextInput(attrs={'null' : 'True','id':"input1" ,'onkeyup':"capitalizeText('input1')"}),
        'highlights' : forms.TextInput(attrs={'null' : 'True','id':"input2" ,'onkeyup':"capitalizeText('input2')"}),
        'backlog_justification' : forms.TextInput(attrs={'null' : 'True','id':"input3" ,'onkeyup':"capitalizeText('input3')"})
        }

class WeekOneForm(ModelForm):
     class Meta:
        model = Week_three_Report
        fields = ['report','status']

class WeekTwoForm(ModelForm):
     class Meta:
        model = Week_two_Report
        fields = ['report','status']

class DipUpdateForm(ModelForm):
     class Meta:
        model = Dip_details
        exclude = () 
        widgets ={
        'project_id' : forms.HiddenInput(attrs={'id' : 'dip_id',}),
        'component': forms.TextInput(attrs={'class':'form-control'}),
        'activities': forms.TextInput(attrs={'class':'form-control'}),
        'objectives': forms.TextInput(attrs={'class':'form-control'}),
        'target_participants': forms.TextInput(attrs={'class':'form-control'}),
        'coverage': forms.TextInput(attrs={'class':'form-control'}),
        'process': forms.TextInput(attrs={'class':'form-control'}),
        'duration': forms.TextInput(attrs={'class':'form-control'}),
        'indicator': forms.TextInput(attrs={'class':'form-control'}),
        'expected_out_come': forms.TextInput(attrs={'class':'form-control'}),
        'mov': forms.TextInput(attrs={'class':'form-control'}),
        
     }




class MonthPlanForm(ModelForm):
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        super(MonthPlanForm, self).__init__(*args, **kwargs)
        self.fields['activity_id'].queryset = Dip_Activities.objects.filter(project_detail_id__project_id = pk)
    class Meta:
        model = Month_Plan
        fields = ['activity_id','strategy','duration','no_Of_Participants','location_Of_Activity','main_Responsibility','supportive_Responsibility','result_Expected'] 
        widgets = {
        'activity_id': forms.Select(choices=['test'],attrs={'class':'form-control'}),
        'strategy': forms.TextInput(attrs={'id':"input1" ,'onkeyup':"capitalizeText('input1')",'class':'form-control'}),
        'component': forms.TextInput(attrs={'id':"input2" ,'onkeyup':"capitalizeText('input2')",'class':'form-control'}),
        'duration': forms.TextInput(attrs={'id':"input3" ,'onkeyup':"capitalizeText('input3')",'class':'form-control'}),
        'no_Of_Participants': forms.TextInput(attrs={'id':"input4" ,'onkeyup':"capitalizeText('input4')",'class':'form-control'}),
        'location_Of_Activity': forms.TextInput(attrs={'id':"input5" ,'onkeyup':"capitalizeText('input5')",'class':'form-control'}),
        'main_Responsibility': forms.TextInput(attrs={'id':"input6" ,'onkeyup':"capitalizeText('input6')",'class':'form-control'}),
        'supportive_Responsibility': forms.TextInput(attrs={'id':"input7" ,'onkeyup':"capitalizeText('input7')",'class':'form-control'}),
        'result_Expected': forms.TextInput(attrs={'id':"input8" ,'onkeyup':"capitalizeText('input8')",'class':'form-control'}),
        }


class WeeklyReportForm(ModelForm):
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        super(WeeklyReportForm, self).__init__(*args, **kwargs)
        self.fields['activity_id'].queryset = Dip_Activities.objects.filter(project_detail_id__project_id = pk)
    class Meta:
        model = Weekly_Report
        fields = ['activity_id','unit','approved_budget','cumulative_progress','cumulative_utilisation','remarks'] 
        widgets = {
        'activity_id': forms.Select(choices=['test'],attrs={'class':'form-control'}),
        'unit': forms.TextInput(attrs={'id':"input1" ,'onkeyup':"capitalizeText('input1')",'class':'form-control'}),
        'approved_budget': forms.TextInput(attrs={'id':"input2" ,'onkeyup':"capitalizeText('input2')",'class':'form-control'}),
        'cumulative_progress': forms.TextInput(attrs={'id':"input7" ,'onkeyup':"capitalizeText('input7')",'class':'form-control'}),
        'cumulative_utilisation': forms.TextInput(attrs={'id':"input8" ,'onkeyup':"capitalizeText('input8')",'class':'form-control'}),
        'remarks': forms.TextInput(attrs={'id':"input9" ,'onkeyup':"capitalizeText('input9')",'class':'form-control'}),
        }


class eventForm(ModelForm):
    class Meta:
        model = Event_Plan
        fields = ['event_name','start_date','end_date','venue','no_of_participants','main_objective','key_event','total_budget','point_person','support_persons','any_imp_point','any_imp_point']
        widgets={
              'event_name': forms.TextInput(attrs={'class':'form-control','id':"input1" ,'onkeyup':"capitalizeText('input1')"}),
              'venue': forms.TextInput(attrs={'class':'form-control','id':"input2" ,'onkeyup':"capitalizeText('input2')"}),
              'start_date': forms.DateInput(attrs={'type' :"date"}),
              'end_date': forms.DateInput(attrs={'type' :"date"}),
              'no_of_participants': forms.TextInput(attrs={'class':'form-control','id':"input5" ,'onkeyup':"capitalizeText('input5')"}),
              'main_objective': forms.TextInput(attrs={'class':'form-control','id':"input6" ,'onkeyup':"capitalizeText('input6')"}),
              'key_event': forms.TextInput(attrs={'class':'form-control','id':"input7" ,'onkeyup':"capitalizeText('input7')"}),
              'total_budget': forms.TextInput(attrs={'class':'form-control','id':"input8" ,'onkeyup':"capitalizeText('input8')"}),
              'point_person': forms.TextInput(attrs={'class':'form-control','id':"input9" ,'onkeyup':"capitalizeText('input9')"}),
              'support_persons': forms.TextInput(attrs={'class':'form-control','id':"input10" ,'onkeyup':"capitalizeText('input10')"}),
              'any_imp_point': forms.TextInput(attrs={'class':'form-control','id':"input11" ,'onkeyup':"capitalizeText('input11')"}),
        }

class MPCForm(ModelForm):
    monthly_project_plan = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, ''), (False, ''))))
    individual_plan_updated = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    individual_worksheet_updated = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    monthly_progress_report_updated = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    outstation_report = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    monthly_budget_submited = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    settlement_completed = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    project_staff_completed_required_project_compliances = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    release_Salary_project_staff_recommend = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    class Meta:
        model = Monthly_Project_Clearance
        fields = ['reporting_month','monthly_project_plan','individual_plan_updated','individual_worksheet_updated','monthly_progress_report_updated','outstation_report','monthly_budget_submited','settlement_completed','project_staff_completed_required_project_compliances','release_Salary_project_staff_recommend','staff_reason']
        widgets={
            'reporting_month': forms.Select(choices=[Monthly_Project_Clearance.MONTH_CHOICES]),
            'staff_reason': forms.TextInput(attrs={'null':'True','class':'form-control','id':"input2" ,'onkeyup':"capitalizeText('input2')"}),
        }


class DipActivitiesForm(ModelForm):
        class Meta:
         model = Dip_Activities
         fields = ['activity_name','objectives','coverage','duration','target_participants']