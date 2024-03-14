from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['email', 'password1', 'password2','first_name', 'last_name' ]

class CategoryForm(ModelForm):
     class Meta:
        model = Project_Category
        exclude = () 
        widgets ={ 
        'Category_name': forms.TextInput(attrs={'class':'form-control','placeholder':"Category Name.."}),
     }


class ProjectForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize the queryset for the 'assigned_to' field
        self.fields['assigned_to'].queryset = User.objects.exclude(is_superuser=True)
        
        # Modify the choices to display first and last names instead of usernames
        self.fields['assigned_to'].choices = [(user.id, f'{user.first_name} {user.last_name}' ) for user in self.fields['assigned_to'].queryset]
        self.fields['assigned_to'].widget.choices = [('', 'Select Project Manager')] + list(self.fields['assigned_to'].widget.choices)[1:]
    class Meta:
        model = Project_DIP
        fields =['project_name','start_date','end_date','assigned_to','donor_name','category_id','budget']
        widgets = {
        'period' : forms.HiddenInput(),
        'project_name': forms.TextInput(attrs={'placeholder' :"Project name...."}),
        'start_date': forms.DateInput(attrs={'type' : 'date','style':'color:black'}),
        'end_date': forms.DateInput(attrs={'type' : 'date','style':'color:black'}),
        'assigned_to' : forms.Select(choices=['test']),
        'donor_name' : forms.TextInput(attrs={'placeholder' :"Donor name...."}),
        'budget' : forms.TextInput(attrs={'placeholder' :"Budget...."}),
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
        fields = ['achievements','target_achived']
        widgets ={
        'achievements' : forms.TextInput(attrs={'null' : 'True','id':"input1" ,'onkeyup':"capitalizeText('input1')"}),
        'target_achived' : forms.NumberInput(attrs={'null' : 'True'})
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
        fields = ['activity_id','strategy','duration','no_Of_Participants','target','location_Of_Activity','main_Responsibility','supportive_Responsibility','result_Expected'] 
        widgets = {
        'activity_id': forms.Select(choices=['test']),
        'strategy': forms.TextInput(attrs={'id':"input1" ,'onkeyup':"capitalizeText('input1')",'class':'form-control'}),
        'component': forms.TextInput(attrs={'id':"input2" ,'onkeyup':"capitalizeText('input2')",'class':'form-control'}),
        'duration': forms.TextInput(attrs={'id':"input3" ,'onkeyup':"capitalizeText('input3')",'class':'form-control'}),
        'target': forms.TextInput(attrs={'class':'form-control'}),
        'no_Of_Participants': forms.TextInput(attrs={'id':"input4" ,'onkeyup':"capitalizeText('input4')",'class':'form-control'}),
        'location_Of_Activity': forms.TextInput(attrs={'id':"input5" ,'onkeyup':"capitalizeText('input5')",'class':'form-control'}),
        'main_Responsibility': forms.TextInput(attrs={'id':"input6" ,'onkeyup':"capitalizeText('input6')",'class':'form-control'}),
        'supportive_Responsibility': forms.TextInput(attrs={'id':"input7" ,'onkeyup':"capitalizeText('input7')",'class':'form-control'}),
        'result_Expected': forms.TextInput(attrs={'id':"input8" ,'onkeyup':"capitalizeText('input8')",'class':'form-control'}),
        }
        labels = {
                'activity_id': 'Activity Name',
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
        'activity_id': forms.Select(choices=['test'],attrs={'class':"box"}),
        'unit': forms.TextInput(attrs={'id':"input1" ,'onkeyup':"capitalizeText('input1')"}),
        'approved_budget': forms.TextInput(attrs={'id':"input2" ,'onkeyup':"capitalizeText('input2')"}),
        'cumulative_progress': forms.TextInput(attrs={'id':"input7" ,'onkeyup':"capitalizeText('input7')"}),
        'cumulative_utilisation': forms.TextInput(attrs={'id':"input8" ,'onkeyup':"capitalizeText('input8')"}),
        'remarks': forms.TextInput(attrs={'id':"input9" ,'onkeyup':"capitalizeText('input9')"}),
        }


class eventForm(ModelForm):
    class Meta:
        model = Event_Plan
        fields = ['event_name','start_date','end_date','venue','no_of_participants','main_objective','key_event','total_budget','point_person','support_persons','any_imp_point']
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
    monthly_project_plan = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
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
        fields = ['monthly_project_plan','individual_plan_updated','individual_worksheet_updated','monthly_progress_report_updated','outstation_report','monthly_budget_submited','settlement_completed','project_staff_completed_required_project_compliances','release_Salary_project_staff_recommend','staff_reason','is_submited']
        widgets={
            'reporting_month': forms.Select(choices=[Monthly_Project_Clearance.MONTH_CHOICES]),
            'staff_reason': forms.TextInput(attrs={'class':'form-control','id':"input2" ,'onkeyup':"capitalizeText('input2')"}),
        }

class DipActivitiesForm(ModelForm):
        class Meta:
         model = Dip_Activities
         fields = ['activity_name','objectives','coverage','duration','target_participants']


class LeaveForm(ModelForm):
    class Meta:
        model = Leave_Statement
        fields = ['total_leaves_allowed','name_of_staff','designation','date_of_joining','remarks']
        widgets={
              'total_leaves_allowed': forms.NumberInput(attrs={'class':'form-control','id':"input1" ,'onkeyup':"capitalizeText('input1')"}),
              'name_of_staff': forms.TextInput(attrs={'class':'form-control','id':"input2" ,'onkeyup':"capitalizeText('input2')"}),
              'designation': forms.TextInput(attrs={'class':'form-control','id':"input3" ,'onkeyup':"capitalizeText('input3')"}),
              'date_of_joining': forms.DateInput(attrs={'type' :"date"}),
              'remarks': forms.TextInput(attrs={'class':'form-control','id':"input5" ,'onkeyup':"capitalizeText('input5')"}),
        }

class MonthlyLeaveForm(ModelForm):
    class Meta:
        model = Leave_Statement
        fields = ['m1_leave','m2_leave','m3_leave','m4_leave','m5_leave','m6_leave','m7_leave','m8_leave','m9_leave','m10_leave','m11_leave','m12_leave']     


class MscForm(ModelForm):
    mpr = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    planning = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    budget = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    settlement_completed = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    case_study = forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    outstation_report= forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    event_report= forms.BooleanField(required=False,initial=False,widget=forms.RadioSelect(choices=((True, 'Yes'), (False, 'No'))))
    class Meta:
        model = Monthly_staff_clearance
        fields = ['name_of_staff','designation','leave_taken_this_month','mpr','planning','budget','settlement_completed','case_study','outstation_report','event_report','any_other']
        widgets={
              'name_of_staff': forms.TextInput(attrs={'class':'form-control','id':"input2" ,'onkeyup':"capitalizeText('input2')"}),
              'designation': forms.TextInput(attrs={'class':'form-control','id':"input3" ,'onkeyup':"capitalizeText('input3')"}),
              'any_other': forms.TextInput(attrs={'id':"input1" ,'onkeyup':"capitalizeText('input1')"}),
              'leave_taken_this_month': forms.DateInput(attrs={'type' :"date"}),
        }

class LeaverequestForm(ModelForm):
    class Meta:
        model = Leave_Application
        fields = ['name_of_staff','designation','leave_requested_from','leave_requested_to','type_of_leave','leave_balance_till_to_date','address','phone_no']
        widgets={
              'total_leaves_allowed': forms.NumberInput(attrs={'class':'form-control','id':"input1" ,'onkeyup':"capitalizeText('input1')"}),
              'name_of_staff': forms.TextInput(attrs={'class':'form-control','id':"input2" ,'onkeyup':"capitalizeText('input2')"}),
              'designation': forms.TextInput(attrs={'class':'form-control','id':"input3" ,'onkeyup':"capitalizeText('input3')"}),
              'leave_requested_from': forms.DateInput(attrs={'type' :"date"}),
              'leave_requested_to': forms.DateInput(attrs={'type' :"date"}),
              'type_of_leave': forms.Select(choices=['Test']),
              'leave_balance_till_to_date': forms.NumberInput(attrs={'type' :"number",'class':'form-control'}),
              'address': forms.TextInput(attrs={'class':'form-control','id':"input4" ,'onkeyup':"capitalizeText('input4')"}),
              'phone_no': forms.NumberInput(attrs={'class':'form-control'}),
        }

class AssetForm(ModelForm):
    class Meta:
        model = Asset
        fields = ['name_of_asset','asset_id_no','unit','status']
        widgets={
              'name_of_asset': forms.TextInput(attrs={'class':'form-control','id':"input1" ,'onkeyup':"capitalizeText('input1')"}),
              'asset_id_no': forms.TextInput(attrs={'class':'form-control'}),
              'status': forms.Select(choices=['Test'],attrs={'class':'form-control'}),
              'unit': forms.NumberInput(attrs={'type' :"number",'class':'form-control'}),
        }

class Ad_clerance_Form(ModelForm):
    class Meta:
        model = Clearance_Admin
        fields = ['name','designation','last_date','location','resignation','programme_remarks','programme_signature','misc_remarks','misc_signature','office_secretary_remarks','office_secretary_signature','administration_remarks','administration_signature','finance_remarks','finance_signature']
        widgets={
              'name': forms.TextInput(attrs={'class':'form-control','id':"input1" ,'onkeyup':"capitalizeText('input1')"}),
              'designation': forms.TextInput(attrs={'class':'form-control'}),
              'location': forms.TextInput(attrs={'class':'form-control'}),
              'resignation': forms.TextInput(attrs={'class':'form-control'}),
              'last_date': forms.DateInput(attrs={'type' :"date"}),
        }


class AppraisalForm(ModelForm):
    class Meta:
        model = Appraisal
        fields = ['name_of_staff','designation','appraisal_period_start_date','appraisal_period_end_date','type_of_appraisal', 'name_of_the_appraisal_authority', 'appraisal_authority_designation','dedication', 'performance', 'cooperation', 'initiative', 'communication', 'teamwork', 'documentation_reporting', 'problem_solving','personality','overall_Rating','recommendation']
        widgets={
            'name_of_staff':forms.TextInput(attrs={'class':'form-control','id':"input1" ,'onkeyup':"capitalizeText('input1')"}),
            'designation':forms.TextInput(attrs={'class':'form-control','id':"input1" ,'onkeyup':"capitalizeText('input1')"}),
            'appraisal_period_start_date':forms.DateInput(attrs={'type' :"date"}),
            'appraisal_period_end_date':forms.DateInput(attrs={'type' :"date"}),
            'type_of_appraisal':forms.Select(choices=['Test'],attrs={'class':'form-control'}), 
            'name_of_the_appraisal_authority':forms.TextInput(attrs={'class':'form-control','id':"input2" ,'onkeyup':"capitalizeText('input2')"}), 
            'appraisal_authority_designation':forms.TextInput(attrs={'class':'form-control','id':"input3" ,'onkeyup':"capitalizeText('input3')"}),
            'dedication': forms.RadioSelect(), 
            'performance': forms.RadioSelect(), 
            'cooperation': forms.RadioSelect(), 
            'initiative': forms.RadioSelect(), 
            'communication': forms.RadioSelect(),
            'teamwork': forms.RadioSelect(), 
            'documentation_reporting': forms.RadioSelect(), 
            'problem_solving': forms.RadioSelect(),
            'personality': forms.RadioSelect(),
            'overall_Rating': forms.RadioSelect(),
            'recommendation':forms.TextInput(attrs={'class':'form-control','id':"input4" ,'onkeyup':"capitalizeText('input4')"}),
         }
        

class pr_clerance_Form(ModelForm):
    class Meta:
        model = Clearance_Programme
        fields = ['name','designation','location']
        widgets={
              'name': forms.TextInput(attrs={'class':'form-control','id':"input1" ,'onkeyup':"capitalizeText('input1')"}),
              'designation': forms.TextInput(attrs={'class':'form-control','id':"input2" ,'onkeyup':"capitalizeText('input2')"}),
              'location': forms.TextInput(attrs={'class':'form-control','id':"input3" ,'onkeyup':"capitalizeText('input3')"}),
        }

class pr_clerance_activity_Form(ModelForm):
    class Meta:
        model = Clearance_Programme_key_activities
        fields = ['activity_name','current_status','way_forward']
        widgets={
              'activity_name': forms.TextInput(attrs={'class':'form-control','id':"input4" ,'onkeyup':"capitalizeText('input4')"}),
              'current_status': forms.TextInput(attrs={'class':'form-control','id':"input5" ,'onkeyup':"capitalizeText('input5')"}),
              'way_forward': forms.TextInput(attrs={'class':'form-control','id':"input6" ,'onkeyup':"capitalizeText('input6')"}),
        }

class OutstationForm(ModelForm):
    class Meta:
        model = OutStation
        fields = ['name','designation','period_of_travel_from','period_of_travel_to','purpose','place_to_be_visited','tentative_programme_during_visit','estimated_travel_cost','means_of_transportation','remarks' ]
        widgets={
              'name': forms.TextInput(attrs={'class':'form-control','id':"input1" ,'onkeyup':"capitalizeText('input1')"}),
              'designation': forms.TextInput(attrs={'class':'form-control','id':"input2" ,'onkeyup':"capitalizeText('input2')"}),
              'purpose': forms.TextInput(attrs={'class':'form-control','id':"input3" ,'onkeyup':"capitalizeText('input3')"}),
              'place_to_be_visited': forms.TextInput(attrs={'class':'form-control','id':"input4" ,'onkeyup':"capitalizeText('input4')"}),
              'tentative_programme_during_visit': forms.TextInput(attrs={'class':'form-control','id':"input5" ,'onkeyup':"capitalizeText('input5')"}),
              'means_of_transportation': forms.TextInput(attrs={'class':'form-control','id':"input6" ,'onkeyup':"capitalizeText('input6')"}),
              'remarks': forms.TextInput(attrs={'class':'form-control','id':"input6" ,'onkeyup':"capitalizeText('input6')"}),
              'period_of_travel_from':forms.DateInput(attrs={'type' :"date"}),
              'period_of_travel_to':forms.DateInput(attrs={'type' :"date"}),
              'estimated_travel_cost':forms.NumberInput(attrs={'type' :"number",'class' :'form-control'})
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Case_study
        fields = ['case_studies']
        widgets ={
            'case_studies': forms.FileInput(attrs={'accept':'.pdf,.doc,.docx','multiple':'True'})
        }



class MonthlyBudgetRequestForm(ModelForm):
    class Meta:
        model = MonthlyBudget
        fields = ['name','designation','programme','budget_head','approved_budget','requsted_budget']
        widgets={
              'name': forms.TextInput(attrs={'id':"input1" ,'onkeyup':"capitalizeText('input1')"}),
              'designation': forms.TextInput(attrs={'id':"input2" ,'onkeyup':"capitalizeText('input2')"}),
              'programme': forms.TextInput(attrs={'id':"input3" ,'onkeyup':"capitalizeText('input3')"}),
              'approved_budget': forms.NumberInput(),
              'requsted_budget': forms.NumberInput(),
        }


class EditUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email','first_name','last_name']

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name']
        widgets={
            'username': forms.TextInput(attrs={'style':"width:95%;"})
            }

class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_no', 'address','designation','gender','profile_pic']
        widgets={
            'address': forms.Textarea(attrs={'style':"width:95%;",'cols':"30",'rows':"5"}),
            'profile_pic': forms.FileInput(attrs={'style':"display: none;",'id':'profile-picture-input','accept':"image/png, image/jpg, image/jpeg"})
            }

    

