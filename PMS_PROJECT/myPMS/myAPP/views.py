from datetime import datetime, timedelta
from django.http import Http404, JsonResponse
from django.utils.timezone import now
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from .forms import ActivityAproveForm, ActivityMatrixAproveForm, ActivityMatrixCeoForm, Ad_clerance_Form, AmRemarkForm, AppraisalForm, AssetForm, CategoryForm, CeoAproveForm, DipActivitiesForm, DipComponentForm, DipIndicatorForm, DipMovForm, DipOutcomeForm, DipProcessForm, DipRemarkForm, DipUpdateForm, DocumentForm, EditProfileForm, EditUserForm, EventPlanAproveForm, EventRemarkForm, LeaveForm, LeaverequestForm, LocationCountForm, MPCForm, MonthlyBudgetRequestForm, MonthlyLeaveForm, MonthlyPlanAproveForm, MonthlyReportUpdateForm, MonthlyachievementForm, MonthlybacklogForm, MonthlyhighlightForm, MscForm, OutstationForm, PlanRemarkForm, ProjectForm, ReportAproveForm, ReportRemarkForm, TimeFrameForm, WeekOneForm, WeekTwoForm, WeeklyReportForm, MonthPlanForm,eventForm, pr_clerance_Form, pr_clerance_activity_Form
from django.contrib import messages
from .forms import  CreateUserForm
from .decorators import admin_only, allowed_users, unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import Group
from django.utils import timezone
from django.shortcuts import HttpResponse, get_object_or_404
from django.core.exceptions import PermissionDenied
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.urls import reverse


def user_belongs_to_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False
    return user.groups.filter(name=group_name).exists()


# login and logout
@unauthenticated_user
def loginPage(request):
    projects = Project_DIP.objects.order_by('-created_at')[:50]
    if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      projectname= request.POST.get('projectname')
      user = authenticate(request, username=username, password=password)
      assigned = Project_DIP.objects.filter(assigned_to = user).values_list('id', flat=True)
      if user is not None:
          if user_belongs_to_group(user,'Project Manager'):
            if projectname != 'null':
              if int(projectname) in assigned:
                login(request, user)
                return redirect('myAPP:pm-home', projectname)
              else:
                messages.info(request, 'You are unauthorized to open this Project')
            else:
                messages.info(request, 'Please Select a Project')
          else:
              login(request, user)
              if user_belongs_to_group(user,'HR Manager'):
                  return redirect('myAPP:hr-home')
              else:
                return redirect('myAPP:masterhome')
      else:
          messages.info(request, 'Username OR password is incorrect')
    return render(request, 'registration/index.html',{"projects":projects})

def logoutUser(request):
	logout(request)
	return redirect('login')

# project_manager landingpage
@login_required(login_url='login')
def home(request,pk):
    project = Project_DIP.objects.get(id=pk)
    projects = Project_DIP.objects.all()
    categories = Project_Category.objects.all()
    user=0
    if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
    else:
        user = 0
    context = {
        'user':user,
        'projects':projects,
        'categories':categories,
        'project':project
        }
    return render(request, 'myAPP/planning-home.html',context)

# ceo landingpage
@login_required(login_url='login')
@allowed_users("CEO")
def masterhome(request):
    user=0
    if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
    else:
        user = 0
    projects = Project_DIP.objects.all()
    profile = Profile.objects.get(user=request.user)
    projects_with_submitted_dip = Project_DIP.objects.filter(
        dip_details__dip_activities__is_dip_submited=True , dip_details__dip_activities__is_dip_approved=False
    ).distinct()
    projects_with_submitted_am = Project_DIP.objects.filter(
        dip_details__dip_activities__is_am_submited=True , dip_details__dip_activities__is_am_approved=False 
    ).distinct()
    projects_with_submitted_plan = Project_DIP.objects.filter(
        dip_details__dip_activities__month_plan__is_plan_submited=True , dip_details__dip_activities__month_plan__is_plan_approved = False
    ).distinct()
    projects_with_submitted_report = Project_DIP.objects.filter(
        dip_details__dip_activities__month_plan__is_report_submited=True , dip_details__dip_activities__month_plan__is_report_approved = False
    ).distinct()
    projects_with_submitted_event = Project_DIP.objects.filter(
        event_plan__is_submited=True , event_plan__is_approved = False
    ).distinct()


    context = {
        'user':user,
        'projects':projects,
        'projects_with_submitted_dip' : projects_with_submitted_dip,
        'projects_with_submitted_am' : projects_with_submitted_am,
        'projects_with_submitted_plan': projects_with_submitted_plan,
        'projects_with_submitted_report' : projects_with_submitted_report,
        'projects_with_submitted_event' : projects_with_submitted_event,
        'profile' : profile
        }
    return render(request, 'myAPP/dashboard_ceo.html',context)

@login_required(login_url='login')
def userhome(request,pk):
    user=0
    if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
    else:
        user = 0
    project = Project_DIP.objects.get(id=pk)
    projects = Project_DIP.objects.all()
    categories = Project_Category.objects.all()
    profile = Profile.objects.get(user=request.user)
    context = {
        'user':user,
        'projects':projects,
        'categories':categories,
        'project' : project,
        'profile': profile
        }
    return render(request, 'myAPP/dashboard_user.html',context)

login_required(login_url='login')
def hrhome(request):
    user=0
    if user_belongs_to_group(request.user,'Hr Manager'):
        user = 1
    else:
        user = 0
    projects = Project_DIP.objects.all()
    categories = Project_Category.objects.all()
    profile = Profile.objects.get(user=request.user)
    context = {
        'user':user,
        'projects':projects,
        'categories':categories,
        'profile': profile
        }
    return render(request, 'myAPP/dashboard_hr.html',context)

@login_required(login_url='login')
@allowed_users("CEO")
def add_user(request):
      form = CreateUserForm(request.POST)
      if request.POST == 'POST':
        form = CreateUserForm(request.POST)  
        if form.is_valid():  
           data = form.save(commit=False)
           data.username = form.email
           data.save()
      else:  
        form = CreateUserForm()  
      context = {  
        'form':form  
      }  
      return render(request,'myAPP/add-user.html',context)

@login_required(login_url='login')
def user_profile(request,pk):
    user=0
    if user_belongs_to_group(request.user,'Project Manager'):
      user = 1
    else:
      user = 0
    project = get_object_or_404(Project_DIP, id=pk)
    u = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=request.user)
    form =  EditUserForm(instance=u)
    profileform = EditProfileForm(instance=profile)
    if request.method == 'POST':
            form =  EditUserForm(request.POST,instance=u)
            profileform = EditProfileForm(request.POST,request.FILES,instance=profile)
            if form.is_valid() and profileform.is_valid():
              old_profile_pic = request.user.profile.profile_pic
              if old_profile_pic:
                  old_path = os.path.join(settings.MEDIA_ROOT, str(old_profile_pic))
                  if default_storage.exists(old_path):
                      default_storage.delete(old_path)
              form.save()
              profileform.save()
              return redirect('myAPP:pm-home' ,project.id)
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile' : profile,
        'user' : user,
        'form' : form,
        'profileform' : profileform,
        'project': project
    }
    return render(request, 'myAPP/profile.html',context)

@login_required(login_url='login')
@admin_only
def ceo_profile(request):
    user=0
    if user_belongs_to_group(request.user,'Project Manager'):
      user = 1
    else:
      user = 0
    projects = Project_DIP.objects.all()
    u = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=request.user)
    form =  EditUserForm(instance=u)
    profileform = EditProfileForm(instance=profile)
    if request.method == 'POST':
            form =  EditUserForm(request.POST,instance=u)
            profileform = EditProfileForm(request.POST,request.FILES,instance=profile)
            if form.is_valid() and profileform.is_valid():
                old_profile_pic = request.user.profile.profile_pic
                if old_profile_pic:
                  old_path = os.path.join(settings.MEDIA_ROOT, str(old_profile_pic))
                  if default_storage.exists(old_path):
                      default_storage.delete(old_path)
                form.save()
                profileform.save()
                return redirect('myAPP:masterhome')
    context = {
        'profile' : profile,
        'user' : user,
        'form' : form,
        'projects' : projects,
        'profileform' : profileform
    }
    return render(request, 'myAPP/profile.html',context)


# ceo adding user,category and project
@login_required(login_url='login')
@admin_only
def add_Category(request):
      form = CategoryForm()
      if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('myAPP:masterhome')
            else:
                form = CategoryForm() 
      return render(request,'myAPP/addcategory.html',{'form': form})

@login_required(login_url='login')
@admin_only
def update_Category(request,pk):
      category = Project_Category.objects.get(pk=pk)
      form = CategoryForm(instance=category)
      if request.method == 'POST':
            form = CategoryForm(request.POST,instance=category)
            if form.is_valid():
                form.save()
                return redirect('myAPP:masterhome')
            else:
                form = CategoryForm() 
      return render(request,'myAPP/addcategory.html',{'form': form})

@login_required(login_url='login')
@admin_only
def add_Project(request):
      projects = Project_DIP.objects.all()
      categories = Project_Category.objects.all()
      form = ProjectForm()
      if request.method == 'POST':
            form = ProjectForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.period = (data.end_date - data.start_date).days
                data.save()
                messages.success(request,'ProjectDIP Generated Successfully')
                return redirect('myAPP:masterhome')
            else:
                form = ProjectForm()   
      return render(request,'myAPP/add-project.html',{'data': form,'projects':projects,
        'categories':categories,}) 

@login_required(login_url='login')
@admin_only
def update_Project(request,pk):
   projects = Project_DIP.objects.all()  
   form = ProjectForm()
   project = Project_DIP.objects.get(pk=pk)
   form = ProjectForm(request.POST or None, instance=project)
   if request.method == 'POST':
    if form.is_valid():
               form.save()  
               messages.success(request,'ProjectDIP updated Successfully')
               return redirect('myAPP:Project-list')
   return render(request,'myAPP/add-project.html',{'data':form,'project':project,'projects':projects}) 

@login_required(login_url='login')
@admin_only
def category_list(request):
      categories = Project_Category.objects.all()
      context = {
          'categories':categories,
          } 
      return render(request,'myAPP/category-list.html',context)

@login_required(login_url='login')
@admin_only
def Projects_list(request):
      projects = Project_DIP.objects.all()
      context = {
          'projects':projects,
          } 
      return render(request,'myAPP/projects-list.html',context) 

@login_required(login_url='login')
@admin_only
def users_list(request):
      users = User.objects.exclude(is_superuser=True)
      context = {
          'users':users,
          } 
      return render(request,'myAPP/users-list.html',context) 


# planning DIP
@login_required(login_url='login')
def add_DIP_Details(request,pk):
      user=0
      if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
      else:
        user = 0
      project = get_object_or_404(Project_DIP, id=pk)
      projects = Project_DIP.objects.all()
      categories = Project_Category.objects.all()
      component = project.dip_details_set.all()
      activities = Dip_Activities.objects.filter(project_detail_id__in=component)
      MyFirstModelFormSet = inlineformset_factory(
        Project_DIP,  # parent model
        Dip_details,  # child model
        DipComponentForm,  # fields in the child model
        extra=0,  # number of extra forms to display
        can_delete= False  # allow deleting forms
      )
      formset = MyFirstModelFormSet
      if request.method == 'POST':
        formset = MyFirstModelFormSet(request.POST)
        if formset.is_valid():
         for form in formset:
                my_first_model = form.save(commit=False)
                my_first_model.Project_DIP = Project_DIP
                my_first_model.project_id = project
                my_first_model.save()
         return redirect('myAPP:add_DIP_Details',project.id) 
        else:
            print(formset.errors)
        if request.method == 'POST' and not formset.is_valid():
            submited=request.POST.getlist('selected_activities')
            for x in submited:
                act = Dip_Activities.objects.get(id=x)
                form = ActivityAproveForm(request.POST,instance=act)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.is_dip_submited = True
                    data.is_dip_rejected = False
                    data.save()
            return redirect('myAPP:add_DIP_Details',project.id) 
      context = {
        "project":project,
        'component': component,
        'formset': formset,
        'activities':activities,
        'user': user,
        'projects': projects,
        'categories':categories
      }
      return render(request,'myAPP/dip.html',context)

@login_required(login_url='login')
@admin_only
def ceo_aproval_dip(request,pk):
      user=0
      if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
      else:
        user = 0
      project = get_object_or_404(Project_DIP, id=pk)
      projects = Project_DIP.objects.all()
      component = project.dip_details_set.all()
      activities = Dip_Activities.objects.filter(project_detail_id__in=component)
      if request.method == 'POST':
        form = CeoAproveForm(request.POST)
        submited=request.POST.getlist('selected_activities')
        for x in submited:
            act = Dip_Activities.objects.get(id=x)
            form = CeoAproveForm(request.POST,instance=act)
            if form.is_valid():
                data = form.save(commit=False)
                data.is_dip_approved = True
                data.is_dip_rejected = False
                data.save()
        acty = Dip_Activities.objects.filter(is_dip_submited = 1 , project_detail_id__project_id =  project)
        for a in acty:
            ac = Dip_Activities.objects.get(id=a.id)
            if a.is_dip_approved == False:
                form2 = ActivityAproveForm(request.POST,instance=ac)
                if form2.is_valid():
                    data = form2.save(commit=False)
                    data.is_dip_submited = False
                    data.is_dip_rejected = True
                    data.save()
        return redirect('myAPP:ceo_aproval_dip',project.id) 
      context = {
        "project":project,
        "projects":projects,
        'component': component,
        'activities':activities,
        'user': user
      }
      return render(request,'myAPP/ceo-dip.html',context)

@login_required(login_url='login')
@admin_only
def dip_remarks(request,pk):
      activities = Dip_Activities.objects.get(id =pk)
      project = get_object_or_404(Project_DIP, id=activities.project_detail_id.project_id.pk)
      form = DipRemarkForm(instance=activities)
      if request.method == 'POST':
        form = DipRemarkForm(request.POST,instance=activities)
        if form.is_valid():
                data = form.save(commit=False)
                data.is_dip_submited = False
                data.is_dip_rejected = True
                data.save() 
                return redirect('myAPP:ceo_aproval_dip',project.id)
        else:
               form = DipRemarkForm(pk=pk)  
      return render(request,'myAPP/dip-remarks.html',{'form': form,'project':project})

@login_required(login_url='login')
def update_component(request, pk):
  component = Dip_details.objects.get(id=pk)
  form = DipComponentForm(instance=component)
  if request.method == 'POST':
    form = DipComponentForm(request.POST,instance=component)
    if form.is_valid():
        form.save()
        return redirect('myAPP:add_DIP_Details', component.project_id.id)
  return render(request, 'myAPP/update_component.html',{'form': form})

@login_required(login_url='login')
def add_Activity(request,pk):
      user=0
      if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
      else:
        user = 0
      component = Dip_details.objects.get(id=pk)
      project = get_object_or_404(Project_DIP, id=component.project_id.id)
      MyFirstModelFormSet = inlineformset_factory(
        Dip_Activities,  # parent model
        Dip_Process,  # child model
        DipProcessForm,  # fields in the child model
        extra=0,  # number of extra forms to display
        can_delete= False  # allow deleting forms
      )
      MySecondModelFormSet = inlineformset_factory(
        Dip_Activities,  # parent model
        Dip_Indicator,  # child model
        DipIndicatorForm,  # fields in the child model
        extra=0,  # number of extra forms to display
        can_delete= False  # allow deleting forms
      )
      MyThirdModelFormSet = inlineformset_factory(
        Dip_Activities,  # parent model
        Dip_expected_out_come,  # child model
        DipOutcomeForm,  # fields in the child model
        extra=0,  # number of extra forms to display
        can_delete= False  # allow deleting forms
      )
      MyFourthModelFormSet = inlineformset_factory(
        Dip_Activities, # parent model
         Dip_mov,  # child model
         DipMovForm,    # fields in the child model
        extra=0,  # number of extra forms to display
        can_delete= False  # allow deleting forms
      )
      formset1 = MyFirstModelFormSet()
      formset2 = MySecondModelFormSet()
      formset3 = MyThirdModelFormSet()
      formset4 = MyFourthModelFormSet()
      if request.method == 'POST':
        formset1 = MyFirstModelFormSet(request.POST)
        formset2 = MySecondModelFormSet(request.POST)
        formset3 = MyThirdModelFormSet(request.POST)
        formset4 = MyFourthModelFormSet(request.POST)
        my_object = Dip_Activities(
            project_detail_id = component,
            activity_name = request.POST.get('activity_name'),
            objectives = request.POST.get('objectives'),
            coverage = request.POST.get('coverage'),
            duration = request.POST.get('duration'),
            target_participants = request.POST.get('target_participants')
        )
        my_object.save()
        if formset1.is_valid():
         for form in formset1:
                my_first_model = form.save(commit=False)
                my_first_model.Dip_Activities = Dip_Activities
                my_first_model.project_activity_id = my_object
                my_first_model.save()
        else:
            print(formset1.errors)

        if formset2.is_valid():
         for form in formset2:
                my_second_model = form.save(commit=False)
                my_second_model.Dip_Activities = Dip_Activities
                my_second_model.project_activity_id = my_object
                my_second_model.save()
        else:
            print(formset2.errors)

        if formset3.is_valid():
         for form in formset3:
                my_Third_model = form.save(commit=False)
                my_Third_model.Dip_Activities = Dip_Activities
                my_Third_model.project_activity_id = my_object
                my_Third_model.save()
        else:
            print(formset3.errors)

        if formset4.is_valid():
         for form in formset4:
                my_Fourth_model = form.save(commit=False)
                my_Fourth_model.Dip_Activities = Dip_Activities
                my_Fourth_model.project_activity_id = my_object
                my_Fourth_model.save()
        else:
            print(formset4.errors) 
        return redirect('myAPP:add_DIP_Details',component.project_id.id) 

      context = {
          'user' : user,
          'project' : project,
          "component": component,
          "formset1":formset1,
          "formset2":formset2,
          "formset3":formset3,
          "formset4":formset4
        }
      return render(request,'myAPP/add-Activity.html', context ) 

@login_required(login_url='login')
def update_Activity(request,pk):
      user=0
      if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
      else:
        user = 0
      activity = Dip_Activities.objects.get(id=pk)
      component = Dip_details.objects.get(id=activity.project_detail_id.id)
      project = get_object_or_404(Project_DIP, id=component.project_id.id)
      MyFirstModelFormSet = inlineformset_factory(
        Dip_Activities,  # parent model
        Dip_Process,  # child model
        DipProcessForm,  # fields in the child model
        extra=0,  # number of extra forms to display
        can_delete= False  # allow deleting forms
      )
      MySecondModelFormSet = inlineformset_factory(
        Dip_Activities,  # parent model
        Dip_Indicator,  # child model
        DipIndicatorForm,  # fields in the child model
        extra=0,  # number of extra forms to display
        can_delete= False  # allow deleting forms
      )
      MyThirdModelFormSet = inlineformset_factory(
        Dip_Activities,  # parent model
        Dip_expected_out_come,  # child model
        DipOutcomeForm,  # fields in the child model
        extra=0,  # number of extra forms to display
        can_delete= False  # allow deleting forms
      )
      MyFourthModelFormSet = inlineformset_factory(
        Dip_Activities, # parent model
         Dip_mov,  # child model
         DipMovForm,    # fields in the child model
        extra=0,  # number of extra forms to display
        can_delete= False  # allow deleting forms
      )
      formset1 = MyFirstModelFormSet(instance=activity)
      formset2 = MySecondModelFormSet(instance=activity)
      formset3 = MyThirdModelFormSet(instance=activity)
      formset4 = MyFourthModelFormSet(instance=activity)
      form = DipActivitiesForm(instance=activity)
      if request.method == 'POST':
            form = DipActivitiesForm(request.POST,instance=activity)
            if form.is_valid():
                data = form.save(commit=False)
                data.project_detail_id = component
                data.save()
            else:
               form = DipActivitiesForm(instance=activity)
      if request.method == 'POST':
        formset1 = MyFirstModelFormSet(request.POST,instance=activity)
        formset2 = MySecondModelFormSet(request.POST,instance=activity)
        formset3 = MyThirdModelFormSet(request.POST,instance=activity)
        formset4 = MyFourthModelFormSet(request.POST,instance=activity)
        form.save()
        if formset1.is_valid():
         for form in formset1:
                my_first_model = form.save(commit=False)
                my_first_model.Dip_Activities = Dip_Activities
                my_first_model.project_activity_id = activity
                my_first_model.save()
        else:
            print(formset1.errors)

        if formset2.is_valid():
         for form in formset2:
                my_second_model = form.save(commit=False)
                my_second_model.Dip_Activities = Dip_Activities
                my_second_model.project_activity_id = activity
                my_second_model.save()
        else:
            print(formset2.errors)

        if formset3.is_valid():
         for form in formset3:
                my_Third_model = form.save(commit=False)
                my_Third_model.Dip_Activities = Dip_Activities
                my_Third_model.project_activity_id = activity
                my_Third_model.save()
        else:
            print(formset3.errors)

        if formset4.is_valid():
         for form in formset4:
                my_Fourth_model = form.save(commit=False)
                my_Fourth_model.Dip_Activities = Dip_Activities
                my_Fourth_model.project_activity_id = activity
                my_Fourth_model.save()
        else:
            print(formset4.errors) 
        return redirect('myAPP:add_DIP_Details',component.project_id.id) 
      context = {
          'user' : user,
          'project' : project,
          "component": component,
          "formset1":formset1,
          "formset2":formset2,
          "formset3":formset3,
          "formset4":formset4,
          'form': form
        }
      return render(request,'myAPP/update_activity.html', context ) 



# planning AM
@login_required(login_url='login')
def index1(request, pk):
    user=0
    if user_belongs_to_group(request.user,'Project Manager'):
      user = 1
    else:
      user = 0
    project = get_object_or_404(Project_DIP, id=pk)
    component = project.dip_details_set.all()
    next_months = []
    current_month = project.start_date.month
    end_month = project.end_date.month
    date1 = datetime.strptime(str(project.start_date), '%Y-%m-%d').date()
    date2 = datetime.strptime(str(project.end_date), '%Y-%m-%d').date()
    if request.method == 'POST':
      submited=request.POST.getlist('selected_activities')
      for x in submited:
        act = Dip_Activities.objects.get(id=x)
        form = ActivityMatrixAproveForm(request.POST,instance=act)
        if form.is_valid():
          data = form.save(commit=False)
          data.is_am_submited = True
          data.is_am_rejected = False
          data.save()
      return redirect('myAPP:index1',project.id)
    
    difference = (date2.year - date1.year) * 12 + (date2.month - date1.month)
    for i in range(0, 12):
        next_month = (current_month + i) % 12  # Calculate the month index
        if next_month == 0:
            next_month = 12  # Handle December (month index 0)
        next_months.append(datetime(project.start_date.year, next_month, 1))
    context = {
        'project': project,
        'component': component,
        'next_months': next_months,
        'user':user
    }
    return render(request, 'myAPP/activity_matrix.html', context)

@login_required(login_url='login')
@admin_only
def ceo_am_approve(request, pk):
    user=0
    if user_belongs_to_group(request.user,'Project Manager'):
      user = 1
    else:
      user = 0
    project = get_object_or_404(Project_DIP, id=pk)
    projects = Project_DIP.objects.all()
    component = project.dip_details_set.all()
    next_months = []
    current_month = project.start_date.month
    date1 = datetime.strptime(str(project.start_date), '%Y-%m-%d').date()
    date2 = datetime.strptime(str(project.end_date), '%Y-%m-%d').date()
    if request.method == 'POST':
      submited=request.POST.getlist('selected_activities')
      for x in submited:
        act = Dip_Activities.objects.get(id=x)
        form = ActivityMatrixCeoForm(request.POST,instance=act)
        if form.is_valid():
          data = form.save(commit=False)
          data.is_am_approved = True
          data.is_am_rejected = False
          data.save()
      acty = Dip_Activities.objects.filter(is_am_submited = 1 , project_detail_id__project_id =  project)
      for a in acty:
        ac = Dip_Activities.objects.get(id=a.id)
        if a.is_am_approved == False:
              form2 = ActivityMatrixAproveForm(request.POST,instance=ac)
              if form2.is_valid():
                    data = form2.save(commit=False)
                    data.is_am_submited = False
                    data.is_am_rejected = True
                    data.save()
      return redirect('myAPP:ceo_am_approve',project.id)

    for i in range(0, 12):
        next_month = (current_month + i) % 12  # Calculate the month index
        if next_month == 0:
            next_month = 12  # Handle December (month index 0)
        next_months.append(datetime(project.start_date.year, next_month, 1))
    context = {
        'project': project,
        'projects':projects,
        'component': component,
        'next_months': next_months,
        'user':user
    }
    return render(request, 'myAPP/ceo-am.html', context)

@login_required(login_url='login')
@admin_only
def am_remarks(request,pk):
      activities = Dip_Activities.objects.get(id =pk)
      project = get_object_or_404(Project_DIP, id=activities.project_detail_id.project_id.pk)
      form = AmRemarkForm(instance=activities)
      if request.method == 'POST':
        form = AmRemarkForm(request.POST,instance=activities)
        if form.is_valid():
                data = form.save(commit=False)
                data.is_am_submited = False
                data.is_am_rejected = True
                data.save() 
                return redirect('myAPP:ceo_am_approve',project.id)
        else:
               form = AmRemarkForm(pk=pk)  
      return render(request,'myAPP/am-remarks.html',{'form': form,'project':project})

@login_required(login_url='login')
def location_count(request, pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  activity = Dip_Activities.objects.get(id=pk)
  project= Project_DIP.objects.get(id=activity.project_detail_id.project_id.id)
  MyFirstModelFormSet = inlineformset_factory(
        Dip_Activities,  # parent model
        Activity_location,  # child model
        LocationCountForm,  # fields in the child model
        extra=1,  # number of extra forms to display
        can_delete= False  # allow deleting forms
      )
  formset = MyFirstModelFormSet
  if request.method == 'POST':
        formset = MyFirstModelFormSet(request.POST)
        if formset.is_valid():
         for form in formset:
                my_first_model = form.save(commit=False)
                my_first_model.Dip_Activities = Dip_Activities
                my_first_model.activity_id = activity
                my_first_model.save()
        else:
            print(formset.errors)
        return redirect('myAPP:index1', activity.project_detail_id.project_id.pk)
  return render(request, 'myAPP/add_count.html', {'formset':formset,'activity':activity,'user':user,'project':project})

@login_required(login_url='login')
def update_location(request, pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  activity = Dip_Activities.objects.get(id=pk)
  project= Project_DIP.objects.get(id=activity.project_detail_id.project_id.id)
  MyFirstModelFormSet = inlineformset_factory(
        Dip_Activities,  # parent model
        Activity_location,  # child model
        LocationCountForm,  # fields in the child model
        extra=0,  # number of extra forms to display
        can_delete= False  # allow deleting forms
      )
  formset = MyFirstModelFormSet(instance=activity)
  if request.method == 'POST':
    formset = MyFirstModelFormSet(request.POST,instance=activity)
    if formset.is_valid():
         for form in formset:
                my_first_model = form.save(commit=False)
                my_first_model.Dip_Activities = Dip_Activities
                my_first_model.activity_id = activity
                my_first_model.save()
    else:
            print(formset.errors)
    return redirect('myAPP:index1', activity.project_detail_id.project_id.pk)
  return render(request, 'myAPP/update-location.html', {'formset':formset,'activity':activity,'user':user,'project':project})

@login_required(login_url='login')
def timeframe(request,pk):
 user=0
 if user_belongs_to_group(request.user,'Project Manager'):
  user = 1
 else:
  user = 0
 activities = Dip_Activities.objects.get(id =pk)
 project= Project_DIP.objects.get(id=activities.project_detail_id.project_id.id)
 form = TimeFrameForm()
 next_months = []
 current_month = activities.project_detail_id.project_id.start_date.month
 for i in range(0, 12):
        next_month = (current_month + i) % 12  # Calculate the month index
        if next_month == 0:
            next_month = 12  # Handle December (month index 0)
        next_months.append(datetime(activities.project_detail_id.project_id.start_date.year, next_month, 1))
 if request.method == 'POST':
            form = TimeFrameForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.activity_id = activities
                data.start_date = activities.project_detail_id.project_id.start_date
                data.save()
                return redirect('myAPP:index1',activities.project_detail_id.project_id.pk)
            else:
                form = TimeFrameForm()   
 return render(request,'myAPP/timeframe.html',{"activities":activities,'form':form,'next_months':next_months,'user':user,'project':project})

@login_required(login_url='login')
def update_timeframe(request,pk):
 activities = Dip_Activities.objects.get(id =pk)
 time = Activity_timeframe.objects.get(activity_id=activities)
 next_months = []
 current_month = time.start_date.month
 for i in range(0, 12):
        next_month = (current_month + i) % 12  # Calculate the month index
        if next_month == 0:
            next_month = 12  # Handle December (month index 0)
        next_months.append(datetime(time.start_date.year, next_month, 1))
 form = TimeFrameForm(instance=time)
 if request.method == 'POST':
    form = TimeFrameForm(request.POST,instance=time)
    if form.is_valid():
               form.save()  
               return redirect('myAPP:index1',activities.project_detail_id.project_id.pk)
 return render(request,'myAPP/timeframe.html',{"activities":activities,'form':form,'next_months':next_months})


# planning monthly plan
@login_required(login_url='login')
def index2(request,pk):
    user=0
    if user_belongs_to_group(request.user,'Project Manager'):
      user = 1
    else:
      user = 0
    project = get_object_or_404(Project_DIP, id=pk)
    month = datetime.today()
    Plans = Month_Plan.objects.filter(activity_id__project_detail_id__project_id = project).filter(month=month.month).filter(year=month.year)
    if request.method == 'POST':
      submited=request.POST.getlist('selected_activities')
      for x in submited:
        mp = Month_Plan.objects.get(id=x)
        form = MonthlyPlanAproveForm(request.POST,instance=mp)
        if form.is_valid():
          data = form.save(commit=False)
          data.is_plan_submited = True
          data.is_plan_rejected = False
          data.save()
      return redirect('myAPP:index2',project.id)
    context= {
        'project':project,
        'Plans' : Plans,
        'month':month,
        'user': user
        }
    return render(request,'myAPP/monthly-plan.html', context)

@login_required(login_url='login')
@admin_only
def ceoplanapproval(request,pk):
    user=0
    if user_belongs_to_group(request.user,'Project Manager'):
      user = 1
    else:
      user = 0
    project = get_object_or_404(Project_DIP, id=pk)
    projects = Project_DIP.objects.all()
    month = datetime.today()
    Plans = Month_Plan.objects.filter(activity_id__project_detail_id__project_id = project)
    if request.method == 'POST':
      submited=request.POST.getlist('selected_activities')
      for x in submited:
        mp = Month_Plan.objects.get(id=x)
        form = MonthlyPlanAproveForm(request.POST,instance=mp)
        if form.is_valid():
          data = form.save(commit=False)
          data.is_plan_approved = True
          data.is_plan_rejected = False
          data.save()
      plan = Month_Plan.objects.filter(is_plan_submited = 1 ,activity_id__project_detail_id__project_id =  project)
      for a in plan:
        ac = Month_Plan.objects.get(id=a.id)
        if a.is_plan_approved == False:
              form2 =  MonthlyPlanAproveForm(request.POST,instance=ac)
              if form2.is_valid():
                    data = form2.save(commit=False)
                    data.is_plan_submited = False
                    data.is_plan_rejected = True
                    data.save()
      return redirect('myAPP:ceo_plan_approve',project.id)
    context= {
        'project':project,
        'projects':projects,
        'Plans' : Plans,
        'month':month,
        'user': user
        }
    return render(request,'myAPP/ceo-plan.html', context)

@login_required(login_url='login')
@admin_only
def plan_remarks(request,pk):
      plan = get_object_or_404(Month_Plan, id=pk)
      project = get_object_or_404(Project_DIP, id=plan.activity_id.project_detail_id.project_id.id)
      form = PlanRemarkForm(instance=plan)
      if request.method == 'POST':
            form = PlanRemarkForm(request.POST,instance=plan)
            if form.is_valid():
                data = form.save(commit=False)
                data.is_plan_submited = False
                data.is_plan_rejected = True
                data.save()
                return redirect('myAPP:ceo_plan_approve', project.id)
            else:
               form = PlanRemarkForm(pk=pk)  
      return render(request,'myAPP/plan-remarks.html',{'form': form,'project':project})

@login_required(login_url='login')
def add_MonthPlan(request,pk):
      user=0
      if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
      else:
        user = 0
      project = get_object_or_404(Project_DIP, id=pk)
      form = MonthPlanForm(pk=pk)
      if request.method == 'POST':
            form = MonthPlanForm(request.POST,pk=pk)
            if form.is_valid():
                data = form.save(commit=False)
                data.month = datetime.today().month
                data.year = datetime.today().year
                data.save()
                return redirect('myAPP:index2', project.id)
            else:
               form = MonthPlanForm(pk=pk)  
      return render(request,'myAPP/add-monthly-Plan.html',{'data': form,'project':project,'user':user}) 

@login_required(login_url='login')
def update_MonthPlan(request,pk):
      user=0
      if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
      else:
        user = 0
      plan = get_object_or_404(Month_Plan, id=pk)
      project = get_object_or_404(Project_DIP, id=plan.activity_id.project_detail_id.project_id.id)
      form = MonthPlanForm(pk=project,instance=plan)
      if request.method == 'POST':
            form = MonthPlanForm(request.POST,pk=project,instance=plan)
            if form.is_valid():
                data = form.save(commit=False)
                data.month = datetime.today().month
                data.year = datetime.today().year
                data.save()
                return redirect('myAPP:index2', project.id)
            else:
               form = MonthPlanForm(pk=pk)  
      return render(request,'myAPP/add-monthly-Plan.html',{'data': form,'plan':plan,'project':project,'user':user}) 


# planning event
@login_required(login_url='login')
def index6(request,pk):
 user=0
 if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
 else:
    user = 0
 project = Project_DIP.objects.get(id=pk)
 events = Event_Plan.objects.filter(project_id = project)
 if request.method == 'POST':
      submited=request.POST.getlist('selected_activities')
      for x in submited:
        event = Event_Plan.objects.get(id=x)
        form = EventPlanAproveForm(request.POST,instance=event)
        if form.is_valid():
          data = form.save(commit=False)
          data.is_submited = True
          data.is_rejected = False
          data.save()
      return redirect('myAPP:index6',project.id)
 return render(request,'myAPP/event-planning.html', {'events': events,'project':project,'user':user})

@login_required(login_url='login')
@admin_only
def ceoevent(request,pk):
 project = Project_DIP.objects.get(id=pk)
 projects = Project_DIP.objects.all()
 events = Event_Plan.objects.filter(project_id = project)
 if request.method == 'POST':
      submited=request.POST.getlist('selected_activities')
      for x in submited:
        event = Event_Plan.objects.get(id=x)
        form = EventPlanAproveForm(request.POST,instance=event)
        if form.is_valid():
          data = form.save(commit=False)
          data.is_approved = True
          data.is_submited = True
          data.is_rejected = False
          data.save()
      plan = Event_Plan.objects.filter(is_submited = 1, project_id =  project)
      for a in plan:
        ac = Event_Plan.objects.get(id=a.id)
        if a.is_approved == False:
              form2 =  EventPlanAproveForm(request.POST,instance=ac)
              if form2.is_valid():
                    data = form2.save(commit=False)
                    data.is_submited = False
                    data.is_rejected = True
                    data.save()
      return redirect('myAPP:ceo_event_approve',project.id)
 return render(request,'myAPP/ceo-event.html', {'events': events,'project':project,'projects':projects,})

@login_required(login_url='login')
@admin_only
def event_remarks(request,pk):
      event = get_object_or_404(Event_Plan, id=pk)
      project = get_object_or_404(Project_DIP, id=event.project_id.id)
      form = EventRemarkForm(instance=event)
      if request.method == 'POST':
            form = EventRemarkForm(request.POST,instance=event)
            if form.is_valid():
                data = form.save(commit=False)
                data.project_id = project
                data.is_submited = False
                data.is_rejected = True
                data.save()
                return redirect('myAPP:ceo_event_approve',project.pk)
            else:
               form = eventForm(instance=event)  
      return render(request,'myAPP/event-remarks.html',{'form': form,'project':project})

@login_required(login_url='login')
def add_event(request,pk):
      user=0
      if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
      else:
        user = 0
      project = get_object_or_404(Project_DIP, id=pk)
      form = eventForm()
      if request.method == 'POST':
            form = eventForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.project_id = project
                data.save()
                return redirect('myAPP:index6',project.pk)
            else:
               form = eventForm()  
      return render(request,'myAPP/add-Event.html',{'data': form,'project':project,'user':user}) 

@login_required(login_url='login')
def update_event(request,pk):
      user=0
      if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
      else:
        user = 0
      event = get_object_or_404(Event_Plan, id=pk)
      project = get_object_or_404(Project_DIP, id=event.project_id.id)
      form = eventForm(instance=event)
      if request.method == 'POST':
            form = eventForm(request.POST,instance=event)
            if form.is_valid():
                data = form.save(commit=False)
                data.project_id = project
                data.save()
                return redirect('myAPP:index6',project.pk)
            else:
               form = eventForm(instance=event)  
      return render(request,'myAPP/add-Event.html',{'data': form,'project':project,'user':user}) 


@login_required(login_url='login')
def budget_requests(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk) 
  projects = Project_DIP.objects.all() 
  budget = MonthlyBudget.objects.filter(project_id=project) 
  date = datetime.today()
  context= {
        'project':project,
        'projects':projects,
        'user': user,
        'budget':budget,
        'date': date
  }
  return render(request,'myAPP/budget-request.html', context)

@login_required(login_url='login')
def add_budget_request(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk)
  form = MonthlyBudgetRequestForm()
  if request.method == 'POST':
            form = MonthlyBudgetRequestForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.project_id = project
                data.month = datetime.today().month
                data.year = datetime.today().year
                data.save()
                return redirect('myAPP:budget_requests', project.id)
            else:
               form = MonthlyBudgetRequestForm()  
  context= {
        'project':project,
        'user': user,
        'form':form,
  }
  return render(request,'myAPP/add-bdget-request.html', context)

@login_required(login_url='login')
def edit_budget_request(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  mbr = get_object_or_404(MonthlyBudget, id=pk)
  project = get_object_or_404(Project_DIP, id=mbr.project_id.id)
  form = MonthlyBudgetRequestForm(instance=mbr)
  if request.method == 'POST':
            form = MonthlyBudgetRequestForm(request.POST,instance=mbr)
            if form.is_valid():
                form.save()
                return redirect('myAPP:budget_requests', project.id)
            else:
               form = MonthlyBudgetRequestForm(instance=mbr)  
  context= {
        'project':project,
        'user': user,
        'form':form,
  }
  return render(request,'myAPP/add-bdget-request.html', context)



@login_required(login_url='login')
def index4(request,pk):
    user=0
    if user_belongs_to_group(request.user,'Project Manager'):
      user = 1
    else:
      user = 0
    project = get_object_or_404(Project_DIP, id=pk)
    projects = Project_DIP.objects.all()
    context= {
        'project':project,
        'user': user,
        'projects':projects
        }
    return render(request,'myAPP/reporting-home.html', context)

@login_required(login_url='login')
def monthly_report(request,pk):
    user=0
    if user_belongs_to_group(request.user,'Project Manager'):
      user = 1
    else:
      user = 0
    project = get_object_or_404(Project_DIP, id=pk)
    month = datetime.today()
    Plans = Month_Plan.objects.filter(activity_id__project_detail_id__project_id = project)
    if request.method == 'POST':
      submited=request.POST.getlist('selected_activities')
      for x in submited:
        mp = Month_Plan.objects.get(id=x)
        form = MonthlyPlanAproveForm(request.POST,instance=mp)
        if form.is_valid():
          data = form.save(commit=False)
          data.is_report_submited = True
          data.is_report_rejected = False
          data.save()
      return redirect('myAPP:monthly-reporting',project.id)
    context= {
        'project':project,
        'Plans' : Plans,
        'month':month,
        'user': user
        }
    return render(request,'myAPP/monthly-report.html', context)

@login_required(login_url='login')
def add_report_achievement(request,pk):
      user=0
      if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
      else:
        user = 0
      plan = get_object_or_404(Month_Plan, id=pk)
      project = get_object_or_404(Project_DIP, id=plan.activity_id.project_detail_id.project_id.id)
      form = MonthlyachievementForm(instance=plan)
      if request.method == 'POST':
            form = MonthlyachievementForm(request.POST,instance=plan)
            if form.is_valid():
                form.save()
                return redirect('myAPP:monthly-reporting', project.id)
            else:
               form = MonthlyachievementForm(instance=plan)  
      return render(request,'myAPP/achivment_form.html',{'form': form,'plan':plan,'project':project,'user':user})

@login_required(login_url='login')
def add_report_highlights(request,pk):
      user=0
      if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
      else:
        user = 0
      plan = get_object_or_404(Month_Plan, id=pk)
      project = get_object_or_404(Project_DIP, id=plan.activity_id.project_detail_id.project_id.id)
      form = MonthlyhighlightForm(instance=plan)
      if request.method == 'POST':
            form = MonthlyhighlightForm(request.POST,instance=plan)
            if form.is_valid():
                form.save()
                return redirect('myAPP:monthly-reporting', project.id)
            else:
               form = MonthlyhighlightForm(instance=plan)  
      return render(request,'myAPP/highlights_form.html',{'form': form,'plan':plan,'project':project,'user':user}) 

@login_required(login_url='login')
def add_report_backlog(request,pk):
      user=0
      if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
      else:
        user = 0
      plan = get_object_or_404(Month_Plan, id=pk)
      project = get_object_or_404(Project_DIP, id=plan.activity_id.project_detail_id.project_id.id)
      form = MonthlybacklogForm(instance=plan)
      if request.method == 'POST':
            form = MonthlybacklogForm(request.POST,instance=plan)
            if form.is_valid():
                form.save()
                return redirect('myAPP:monthly-reporting', project.id)
            else:
               form = MonthlybacklogForm(instance=plan)  
      return render(request,'myAPP/backlog_form.html',{'form': form,'plan':plan,'project':project,'user':user})  

@login_required(login_url='login')
def update_report(request,pk):
      user=0
      if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
      else:
        user = 0
      plan = get_object_or_404(Month_Plan, id=pk)
      project = get_object_or_404(Project_DIP, id=plan.activity_id.project_detail_id.project_id.id)
      form = MonthlyReportUpdateForm(instance=plan)
      if request.method == 'POST':
            form = MonthlyReportUpdateForm(request.POST,instance=plan)
            if form.is_valid():
                form.save()
                return redirect('myAPP:monthly-reporting', project.id)
            else:
               form = MonthlyReportUpdateForm(instance=plan)  
      return render(request,'myAPP/report-update.html',{'form': form,'plan':plan,'project':project,'user':user}) 

@login_required(login_url='login')
@admin_only
def ceoreportapproval(request,pk):
    user=0
    if user_belongs_to_group(request.user,'Project Manager'):
      user = 1
    else:
      user = 0
    project = get_object_or_404(Project_DIP, id=pk)
    projects = Project_DIP.objects.all()
    month = datetime.today()
    Plans = Month_Plan.objects.filter(activity_id__project_detail_id__project_id = project)
    if request.method == 'POST':
      submited=request.POST.getlist('selected_activities')
      for x in submited:
        mp = Month_Plan.objects.get(id=x)
        form = ReportAproveForm(request.POST,instance=mp)
        if form.is_valid():
          data = form.save(commit=False)
          data.is_report_approved = True
          # data.is_report_submited = True
          data.is_report_rejected = False
          data.save()
      plan = Month_Plan.objects.filter(is_report_submited = 1, activity_id__project_detail_id__project_id =  project)
      for a in plan:
        ac = Month_Plan.objects.get(id=a.id)
        if a.is_report_approved == False:
              form2 =  ReportAproveForm(request.POST,instance=ac)
              if form2.is_valid():
                    data = form2.save(commit=False)
                    data.is_report_submited = False
                    data.is_report_rejected = True
                    data.save()
      return redirect('myAPP:ceo_report_approve',project.id)
    context= {
        'project':project,
        'projects':projects,
        'Plans' : Plans,
        'month':month,
        'user': user
        }
    return render(request,'myAPP/ceo-report.html', context)

@login_required(login_url='login')
@admin_only
def report_remarks(request,pk):
      plan = get_object_or_404(Month_Plan, id=pk)
      project = get_object_or_404(Project_DIP, id=plan.activity_id.project_detail_id.project_id.id)
      form = ReportRemarkForm(instance=plan)
      if request.method == 'POST':
            form = ReportRemarkForm(request.POST,instance=plan)
            if form.is_valid():
                data = form.save(commit=False)
                data.is_report_submited = False
                data.is_report_rejected = True
                data.save()
                return redirect('myAPP:ceo_report_approve', project.id)
            else:
               form = ReportRemarkForm(pk=pk)  
      return render(request,'myAPP/report-remarks.html',{'form': form,'project':project})



@login_required(login_url='login')
def weekly_report(request,pk):
    user=0
    if user_belongs_to_group(request.user,'Project Manager'):
      user = 1
    else:
      user = 0
    project = get_object_or_404(Project_DIP, id=pk)
    projects = Project_DIP.objects.all()
    month = datetime.today()
    Plans = Weekly_Report.objects.filter(activity_id__project_detail_id__project_id = project).filter(month=month.month).filter(year=month.year)
    context= {
        'project':project,
        'projects':projects,
        'user': user,
        'Plans': Plans,
        'month': month,
        }
    return render(request,'myAPP/week-report.html', context)

@login_required(login_url='login')
def add_WeeklyReport(request,pk):
      user=0
      if user_belongs_to_group(request.user,'Project Manager'):
        user = 1
      else:
        user = 0
      project = get_object_or_404(Project_DIP, id=pk)
      form = WeeklyReportForm(pk=pk)
      context= {
          'form': form,
          'project':project,
          'user':user
          }
      return render(request,'myAPP/add-weekly.html',context) 

@login_required(login_url='login')
def create_weekly_report(request,pk):
    project = get_object_or_404(Project_DIP, id=pk)
    if request.method == 'POST': 
        form = WeeklyReportForm(request.POST,pk=pk)  
        data = form.save(commit=False)
        data.month = datetime.today().month
        data.year = datetime.today().year
        data.save()     
        # Create the Week_one_Report instance
        week_one_report = Week_one_Report.objects.create(
            weekly_Report_id=data,
            report=request.POST.get('week_one_report'),
            status=request.POST.get('week_one_status')
        )
        
        # Create the Week_two_Report instance
        week_two_report = Week_two_Report.objects.create(
            weekly_Report_id=data,
            report=request.POST.get('week_two_report'),
            status=request.POST.get('week_two_status')
        )
        
        # Create the Week_three_Report instance
        week_three_report = Week_three_Report.objects.create(
            weekly_Report_id=data,
            report=request.POST.get('week_three_report'),
            status=request.POST.get('week_three_status')
        )
        
        # Create the Week_four_Report instance
        week_four_report = Week_four_Report.objects.create(
            weekly_Report_id=data,
            report=request.POST.get('week_four_report'),
            status=request.POST.get('week_four_status')
        )
        
        # Create the Week_five_Report instance
        week_five_report = Week_five_Report.objects.create(
            weekly_Report_id=data,
            report=request.POST.get('week_five_report'),
            status=request.POST.get('week_five_status')
        )
        
        # Return a success response
        return redirect('myAPP:weekly-report', project.id)
    
    # Return an error response if the request method is not POST
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required(login_url='login')
def update_WeeklyReport(request,pk):
      plan = get_object_or_404(Weekly_Report, id=pk)
      project = get_object_or_404(Project_DIP, id=plan.activity_id.project_detail_id.project_id.id)
      form = WeeklyReportForm(pk=project,instance=plan)
      one = Week_one_Report.objects.get(weekly_Report_id=plan)
      two = Week_two_Report.objects.get(weekly_Report_id=plan)
      three = Week_three_Report.objects.get(weekly_Report_id=plan)
      four = Week_four_Report.objects.get(weekly_Report_id=plan)
      five = Week_five_Report.objects.get(weekly_Report_id=plan)
      context= {
          'form': form,
          'project':project,
          'plan':plan,
          'week_one_report': one,
          'week_two_report': two,
          'week_three_report': three,
          'week_four_report': four,
          'week_five_report': five,
          } 
      return render(request,'myAPP/weekly-update.html',context) 

@login_required(login_url='login')
def update_weekly_report(request, pk):
    plan = get_object_or_404(Weekly_Report, id=pk)
    project = get_object_or_404(Project_DIP, id=plan.activity_id.project_detail_id.project_id.id)
    if request.method == 'POST':
        form = WeeklyReportForm(request.POST,pk=project,instance=plan)  
        if form.is_valid():        
        # Update the fields 
            data = form.save(commit=False)
            data.save()    
        
        # Update the Week_one_Report instance
            week_one_report = Week_one_Report.objects.get(weekly_Report_id=data)
            week_one_report.report = request.POST.get('week_one_report')
            week_one_report.status = request.POST.get('week_one_status')
            week_one_report.save()
        
            # Update the Week_two_Report instance
            week_two_report = Week_two_Report.objects.get(weekly_Report_id=data)
            week_two_report.report = request.POST.get('week_two_report')
            week_two_report.status = request.POST.get('week_two_status')
            week_two_report.save()
            
            # Update the Week_three_Report instance
            week_three_report = Week_three_Report.objects.get(weekly_Report_id=data)
            week_three_report.report = request.POST.get('week_three_report')
            week_three_report.status = request.POST.get('week_three_status')
            week_three_report.save()
            
            # Update the Week_four_Report instance
            week_four_report = Week_four_Report.objects.get(weekly_Report_id=data)
            week_four_report.report = request.POST.get('week_four_report')
            week_four_report.status = request.POST.get('week_four_status')
            week_four_report.save()
            
            # Update the Week_five_Report instance
            week_five_report = Week_five_Report.objects.get(weekly_Report_id=data)
            week_five_report.report = request.POST.get('week_five_report')
            week_five_report.status = request.POST.get('week_five_status')
            week_five_report.save()
            
            return redirect('myAPP:weekly-report', project.id)
    print(form.errors)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required(login_url='login')
def upload_document(request,pk):
    user=0
    if user_belongs_to_group(request.user,'Project Manager'):
      user = 1
    else:
      user = 0
    project = get_object_or_404(Project_DIP,id=pk)
    projects = Project_DIP.objects.all()
    current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    documents_this_month = Case_study.objects.filter(project_id=project, uploaded_at__gte=current_month_start)
    case_studies = Case_study.objects.filter(project_id=project,uploaded_at__month = str(datetime.today().month))
    if request.method == 'POST':
        if documents_this_month.count() >= 5:
            return render(request, 'upload_limit_exceeded.html')
        else:
         form = DocumentForm(request.POST, request.FILES)
         if form.is_valid():
            document = form.save(commit=False)
            document.project_id = project
            document.save()
            return redirect('myAPP:case-studies',project.id)
    else:
        form = DocumentForm()

    context = {
        'form': form,
        'project':  project,
        'case_studies': case_studies,
        'projects' : projects,
        'user': user 
        }
    return render(request, 'myApp/case_study.html', context)

@login_required(login_url='login')
def download_document(request, document_id):
    document = get_object_or_404(Case_study, id=document_id)
    try:
        with open(document.case_studies.path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="{document.project_id.project_name}{document.id}.docx"'
            return response
    except FileNotFoundError:
        raise Http404("File not found")

def display_docs(request,document_id):
    pdfs = get_object_or_404(Case_study, id=document_id)
    return render(request, 'myAPP/view_casestudies.html', {'pdfs': pdfs})


@login_required(login_url='login')
def complince_home(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk)
  projects = Project_DIP.objects.all()
  context= {
        'project':project,
        'user': user,
        'projects':projects,
  }
  return render(request,'myAPP/complince-home.html', context)

@login_required(login_url='login')
def project_clearance(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk) 
  month = datetime.today()
  pc = Monthly_Project_Clearance.objects.filter(project_id=project).filter(reporting_month=month.month)
  context= {
        'project':project,
        'user': user,
        'pc':pc
  }
  return render(request,'myAPP/mpc.html', context)

@login_required(login_url='login')
def add_project_clearance(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk)
  form = MPCForm()
  if request.method == 'POST':
            form = MPCForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.project_id = project
                data.save()
                return redirect('myAPP:mpc-report', project.id)
            else:
               form = MPCForm()  
  context= {
        'project':project,
        'user': user,
        'form':form
  }
  return render(request,'myAPP/add-monthly-clearance.html', context)

@login_required(login_url='login')
def leaves(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk)
  next_months = []
  for i in range(0, 12):
        next_month = (project.start_date.month + i) % 12  # Calculate the month index
        if next_month == 0:
            next_month = 12  # Handle December (month index 0)
        next_months.append(datetime(project.start_date.year, next_month, project.start_date.day)) 
  leaves = Leave_Statement.objects.filter(project_id=project) 
  context= {
        'project':project,
        'user': user,
        'leaves':leaves,
        'next_months': next_months
  }
  return render(request,'myAPP/leave.html', context)

@login_required(login_url='login')
def add_leaves(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk)
  form = LeaveForm()
  if request.method == 'POST':
            form = LeaveForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.project_id = project
                data.total_leaves_remaining = data.total_leaves_allowed
                data.save()
                return redirect('myAPP:leaves', project.id)
            else:
               form = LeaveForm()  
  context= {
        'project':project,
        'user': user,
        'form':form,
  }
  return render(request,'myAPP/add-leave.html', context)

@login_required(login_url='login')
def add_leaves_monthly(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  leave = get_object_or_404(Leave_Statement, id=pk)
  project = get_object_or_404(Project_DIP, id=leave.project_id.id)
  next_months = []
  for i in range(0, 12):
        next_month = (project.start_date.month + i) % 12  # Calculate the month index
        if next_month == 0:
            next_month = 12  # Handle December (month index 0)
        next_months.append(datetime(project.start_date.year, next_month, project.start_date.day)) 
  form = MonthlyLeaveForm(instance=leave)
  if request.method == 'POST':
            form = MonthlyLeaveForm(request.POST,instance=leave)
            if form.is_valid():
                data = form.save(commit=False)
                data.total_leaves_remaining = data.total_leaves_allowed - (data.m1_leave+data.m2_leave+data.m3_leave+data.m4_leave+data.m5_leave+data.m6_leave+data.m7_leave+data.m8_leave+data.m9_leave+data.m10_leave+data.m11_leave+data.m12_leave)
                data.save()
                return redirect('myAPP:leaves', project.id)
            else:
               print(form.errors)
               form = MonthlyLeaveForm(instance=leave)  
  context= {
        'project':project,
        'user': user,
        'form':form,
        'next_months': next_months
  }
  return render(request,'myAPP/add-leave-monthly.html', context)

@login_required(login_url='login')
def msc(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk) 
  msc = Monthly_staff_clearance.objects.filter(project_id=project) 
  date = datetime.today()
  context= {
        'project':project,
        'user': user,
        'msc':msc,
        'date': date
  }
  return render(request,'myAPP/msc.html', context)

@login_required(login_url='login')
def add_msc(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk)
  form = MscForm()
  if request.method == 'POST':
            form = MscForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.project_id = project
                data.month = datetime.today().month
                data.year = datetime.today().year
                data.save()
                return redirect('myAPP:msc', project.id)
            else:
               form = LeaveForm()  
  context= {
        'project':project,
        'user': user,
        'form':form,
  }
  return render(request,'myAPP/add-msc.html', context)

@login_required(login_url='login')
def update_msc(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  msc =  get_object_or_404(Monthly_staff_clearance , id=pk)
  project = get_object_or_404(Project_DIP, id=msc.project_id.id)
  form = MscForm(instance=msc)
  if request.method == 'POST':
            form = MscForm(request.POST,instance=msc)
            if form.is_valid():
                form.save()
                return redirect('myAPP:msc', project.id)
            else:
               form = LeaveForm()  
  context= {
        'project':project,
        'user': user,
        'form':form,
  }
  return render(request,'myAPP/add-msc.html', context)


@login_required(login_url='login')
def governance_home(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk)
  projects = Project_DIP.objects.all()
  categories = Project_Category.objects.all()
  activities = Dip_Activities.objects.all()
  monthlyplans = Month_Plan.objects.all()
  eventplans = Event_Plan.objects.all()
  context= {
        'project':project,
        'user': user,
        'projects':projects,
        'categories':categories,
        'activities': activities,
        'monthlyplans':monthlyplans,
        'eventplans':eventplans
  }
  return render(request,'myAPP/governance-home.html', context)

@login_required(login_url='login')
def leave_application(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk) 
  La = Leave_Application.objects.filter(project_id=project)
  context= {
        'project':project,
        'user': user,
        'leave_applications':La
  }
  return render(request,'myAPP/leave_application_list.html', context)

@login_required(login_url='login')
def add_leave_application(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk) 
  form = LeaverequestForm()
  if request.method == 'POST':
            form = LeaverequestForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.project_id = project
                data.save()
                return redirect('myAPP:leave-application', project.id)
            else:
               form = LeaverequestForm() 
  context= {
        'project':project,
        'user': user,
        'form': form,
  }
  return render(request,'myAPP/add-leave-application.html', context)

@login_required(login_url='login')
def edit_leave_application(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  leave = get_object_or_404(Leave_Application, id=pk) 
  project = get_object_or_404(Project_DIP, id=leave.project_id.id) 
  form = LeaverequestForm(instance=leave)
  if request.method == 'POST':
            form = LeaverequestForm(request.POST,instance=leave)
            if form.is_valid():
                form.save()
                return redirect('myAPP:leave-application', project.id)
            else:
               form = LeaverequestForm(instance=leave) 
  context= {
        'project':project,
        'user': user,
        'form': form,
  }
  return render(request,'myAPP/add-leave-application.html', context)

@login_required(login_url='login')
def appraisals(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk) 
  appraisals = Appraisal.objects.filter(project_id=project)
  context= {
        'project':project,
        'user': user,
        'appraisals':appraisals
  }
  return render(request,'myAPP/appraisal.html', context)

@login_required(login_url='login')
def add_appraisal(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk) 
  form = AppraisalForm()
  x = request.POST.get('rg1')
  if request.method == 'POST':
    form = AppraisalForm(request.POST)
    if form.is_valid():
      data = form.save(commit=False)
      data.project_id = project
      data.save()
      return redirect('myAPP:appraisal', project.id)
    else:
      form = AppraisalForm() 
  context= {
        'project':project,
        'user': user,
        'form': form
  }
  return render(request,'myAPP/add-appraisal.html', context)

@login_required(login_url='login')
def assets(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk) 
  assets = Asset.objects.filter(project_id=project)
  context= {
        'project':project,
        'user': user,
        'assets':assets
  }
  return render(request,'myAPP/assets.html', context)

@login_required(login_url='login')
def add_asset(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk) 
  form = AssetForm()
  if request.method == 'POST':
            form = AssetForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.project_id = project
                data.save()
                return redirect('myAPP:assets', project.id)
            else:
               form = AssetForm() 
  context= {
        'project':project,
        'user': user,
        'form': form,
  }
  return render(request,'myAPP/add-asset.html', context)

@login_required(login_url='login')
def update_asset(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  asset = get_object_or_404(Asset, id=pk) 
  project = get_object_or_404(Project_DIP, id=asset.project_id.id) 
  form = AssetForm(instance=asset)
  if request.method == 'POST':
            form = AssetForm(request.POST,instance=asset)
            if form.is_valid():
              form.save()
              return redirect('myAPP:assets', project.id)
            else:
               form = AssetForm(instance=asset) 
  context= {
        'project':project,
        'user': user,
        'form': form,
  }
  return render(request,'myAPP/add-asset.html', context)

@login_required(login_url='login')
def clearance_admin(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk) 
  ca = Clearance_Admin.objects.filter(project_id=project)
  context= {
        'project':project,
        'user': user,
        'cas': ca
  }
  return render(request,'myAPP/clearance_admin.html', context)

@login_required(login_url='login')
def add_admin_clearance(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk) 
  form = Ad_clerance_Form()
  if request.method == 'POST':
    form = Ad_clerance_Form(request.POST)
    if form.is_valid():
      data = form.save(commit=False)
      data.project_id = project
      data.save()
      return redirect('myAPP:clearance-admin', project.id)
    else:
      form = Ad_clerance_Form() 
  context= {
        'project':project,
        'user': user,
        'form': form,
  }
  return render(request,'myAPP/add-clearance_admin.html', context)

@login_required(login_url='login')
def clearance_programme(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk) 
  ca = Clearance_Programme.objects.filter(project_id=project)
  context= {
        'project':project,
        'user': user,
        'cas': ca
  }
  return render(request,'myAPP/clearance_programme.html', context)

@login_required(login_url='login')
def add_programme_clearance(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk)
  MyFirstModelFormSet = inlineformset_factory(
        Clearance_Programme,  # parent model
        Clearance_Programme_key_activities,  # child model
        pr_clerance_activity_Form,  # fields in the child model
        extra=0,  # number of extra forms to display
        can_delete= False  # allow deleting forms
      )
  formset = MyFirstModelFormSet()
  form = pr_clerance_Form()
  if request.method == 'POST':
        formset = MyFirstModelFormSet(request.POST)
        form = pr_clerance_Form(request.POST)
        if form.is_valid() and formset.is_valid():
          data = form.save(commit=False)
          data.project_id = project
          data.save()
          for form in formset:
                model = form.save(commit=False)
                model.Clearance_Programme = Clearance_Programme
                model.cp_id = data
                model.save()
        else:
            print(formset.errors) 
        return redirect('myAPP:clearance-programme', project.id) 
  context= {
        'project':project,
        'user': user,
        'form': form,
        'formset': formset, 
  }
  return render(request,'myAPP/add-clearance_programme.html', context)

@login_required(login_url='login')
def leaving_station(request,pk):
  user=0
  if user_belongs_to_group(request.user,'Project Manager'):
    user = 1
  else:
    user = 0
  project = get_object_or_404(Project_DIP, id=pk) 
  ls = OutStation.objects.filter(project_id=project)
  context= {
        'project':project,
        'user': user,
        'requests': ls
  }
  return render(request,'myAPP/outstation_permission.html', context)

@login_required(login_url='login')
def add_leaving_station(request,pk):
  project = get_object_or_404(Project_DIP, id=pk) 
  form = OutstationForm()
  if request.method == 'POST':
    form = OutstationForm(request.POST)
    if form.is_valid():
      data = form.save(commit=False)
      data.project_id = project
      data.save()
      return redirect('myAPP:leaving-station', project.id)
    else:
      form = OutstationForm()
  context= {
        'project':project,
        'form': form,
  }
  return render(request,'myAPP/add-outstation-reqest.html', context)
























