from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils.timezone import now
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Activity_location, Activity_timeframe, Dip_Activities, Dip_Indicator, Dip_Process, Dip_expected_out_come, Dip_mov, Project_Category, Project_DIP,Month_Plan,Dip_details,Event_Plan, Week_five_Report, Week_four_Report, Week_one_Report, Week_three_Report, Week_two_Report, Weekly_Report
from .forms import ActivityAproveForm, ActivityMatrixAproveForm, ActivityMatrixCeoForm, AmRemarkForm, CategoryForm, CeoAproveForm, DipActivitiesForm, DipComponentForm, DipIndicatorForm, DipMovForm, DipOutcomeForm, DipProcessForm, DipRemarkForm, DipUpdateForm, EventPlanAproveForm, EventRemarkForm, LocationCountForm, MPCForm, MonthlyPlanAproveForm, MonthlyReportUpdateForm, MonthlyachievementForm, MonthlybacklogForm, MonthlyhighlightForm, PlanRemarkForm, ProjectForm, ReportAproveForm, ReportRemarkForm, TimeFrameForm, WeekOneForm, WeekTwoForm, WeeklyReportForm, MonthPlanForm,eventForm
from django.contrib import messages
from .forms import  CreateUserForm
from .decorators import admin_only, allowed_users, unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import Group


@login_required(login_url='login')
def home(request,pk):
    project = Project_DIP.objects.get(id=pk)
    projects = Project_DIP.objects.all()
    categories = Project_Category.objects.all()
    user=0
    if user_belongs_to_group(request.user,'ProjectManager'):
        user = 1
    else:
        user = 0
    context = {
        'user':user,
        'projects':projects,
        'categories':categories,
        'project':project
        }
    return render(request, 'myAPP/home.html',context)

@login_required(login_url='login')
@allowed_users("CEO")
def masterhome(request):
    user=0
    if user_belongs_to_group(request.user,'ProjectManager'):
        user = 1
    else:
        user = 0
    projects = Project_DIP.objects.all()
    categories = Project_Category.objects.all()
    activities = Dip_Activities.objects.all()
    monthlyplans = Month_Plan.objects.all()
    eventplans = Event_Plan.objects.all()
    context = {
        'user':user,
        'projects':projects,
        'categories':categories,
        'activities':activities,
        'monthlyplans': monthlyplans,
        'eventplans':eventplans
        }
    return render(request, 'myAPP/home1.html',context)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
        context = {'form':form}
        return render(request, 'registration/signup.html', context)

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
          if user_belongs_to_group(user,'ProjectManager'):
            if projectname != 'null':
              if int(projectname) in assigned:
                login(request, user)
                return redirect('myAPP:home', projectname)
              else:
                messages.info(request, 'You are unauthorized to open this Project')
            else:
                messages.info(request, 'Please Select a Project')
          else:
              login(request, user)
              return redirect('myAPP:masterhome')
      else:
          messages.info(request, 'Username OR password is incorrect')
    return render(request, 'registration/login.html',{"projects":projects})

def logoutUser(request):
	logout(request)
	return redirect('login')

def user_belongs_to_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False
    return user.groups.filter(name=group_name).exists()



@login_required(login_url='login')
def index(request):
 x=0
 if user_belongs_to_group(request.user,'CEO'):
     x = 1
     projects = Project_DIP.objects.order_by('-created_at')[:50]
 elif user_belongs_to_group(request.user,'ProjectManager'):
     user = request.user.id
     projects = Project_DIP.objects.select_related('assigned_to').filter(assigned_to = user).order_by('-created_at')[:50]
 else:
     projects = Project_DIP.objects.order_by('-created_at')[:50]
 return render(request,'myAPP/index.html', {'projects': projects,'user':x})

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
def add_Project(request):
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
      return render(request,'myAPP/getdata.html',{'data': form}) 

@login_required(login_url='login')
@admin_only
def update_Project(request,project_id):  
   form = ProjectForm()
   project = Project_DIP.objects.get(pk=project_id)
   form = ProjectForm(request.POST or None, instance=project)
   if request.method == 'POST':
    if form.is_valid():
               form.save()  
               messages.success(request,'ProjectDIP updated Successfully')
               return redirect('myAPP:index')
   return render(request,'myAPP/updateProject.html',{'data':form}) 



@login_required(login_url='login')
def add_DIP_Details(request,pk):
      user=0
      if user_belongs_to_group(request.user,'ProjectManager'):
        user = 1
      else:
        user = 0
      project = get_object_or_404(Project_DIP, id=pk)
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
        "projects":project,
        'component': component,
        'formset': formset,
        'activities':activities,
        'user': user
      }
      return render(request,'myAPP/getdataDip.html',context)

@login_required(login_url='login')
@admin_only
def ceo_aproval_dip(request,pk):
      user=0
      if user_belongs_to_group(request.user,'ProjectManager'):
        user = 1
      else:
        user = 0
      project = get_object_or_404(Project_DIP, id=pk)
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
        acty = Dip_Activities.objects.filter(is_dip_submited = 1)
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
        "projects":project,
        'component': component,
        'activities':activities,
        'user': user
      }
      return render(request,'myAPP/ceo-dip.html',context)

@login_required(login_url='login')
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
      component = Dip_details.objects.get(id=pk)
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
          "component": component,
          "formset1":formset1,
          "formset2":formset2,
          "formset3":formset3,
          "formset4":formset4
        }
      return render(request,'myAPP/getdataActivity.html', context ) 

@login_required(login_url='login')
def update_Activity(request,pk):
      activity = Dip_Activities.objects.get(id=pk)
      component = Dip_details.objects.get(id=activity.project_detail_id.id)
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
          "component": component,
          "formset1":formset1,
          "formset2":formset2,
          "formset3":formset3,
          "formset4":formset4,
          'form': form
        }
      return render(request,'myAPP/update_activity.html', context ) 



@login_required(login_url='login')
def index1(request, pk):
    user=0
    if user_belongs_to_group(request.user,'ProjectManager'):
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
    return render(request, 'myAPP/index1.html', context)

@login_required(login_url='login')
@admin_only
def ceo_am_approve(request, pk):
    user=0
    if user_belongs_to_group(request.user,'ProjectManager'):
      user = 1
    else:
      user = 0
    project = get_object_or_404(Project_DIP, id=pk)
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
      acty = Dip_Activities.objects.filter(is_am_submited = 1)
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
        'component': component,
        'next_months': next_months,
        'user':user
    }
    return render(request, 'myAPP/ceo-am.html', context)

@login_required(login_url='login')
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
  activity = Dip_Activities.objects.get(id=pk)
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
  return render(request, 'myAPP/add_count.html', {'formset':formset,'activity':activity})

@login_required(login_url='login')
def update_location(request, pk):
  activity = Dip_Activities.objects.get(id=pk)
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
  return render(request, 'myAPP/update-location.html', {'formset':formset,'activity':activity})

@login_required(login_url='login')
def timeframe(request,pk):
 activities = Dip_Activities.objects.get(id =pk)
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
 return render(request,'myAPP/timeframe.html',{"activities":activities,'form':form,'next_months':next_months})

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



@login_required(login_url='login')
def index2(request,pk):
    user=0
    if user_belongs_to_group(request.user,'ProjectManager'):
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
    return render(request,'myAPP/index2.html', context)

@login_required(login_url='login')
@admin_only
def ceoplanapproval(request,pk):
    user=0
    if user_belongs_to_group(request.user,'ProjectManager'):
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
          data.is_plan_approved = True
          data.is_plan_rejected = False
          data.save()
      plan = Month_Plan.objects.filter(is_plan_submited = 1)
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
        'Plans' : Plans,
        'month':month,
        'user': user
        }
    return render(request,'myAPP/ceo-plan.html', context)

@login_required(login_url='login')
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
      return render(request,'myAPP/getdataPlan.html',{'data': form,'project':project}) 

@login_required(login_url='login')
def update_MonthPlan(request,pk):
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
      return render(request,'myAPP/getdataPlan.html',{'data': form,'plan':plan,'project':project}) 



@login_required(login_url='login')
def index6(request,pk):
 user=0
 if user_belongs_to_group(request.user,'ProjectManager'):
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
 return render(request,'myAPP/index6.html', {'events': events,'project':project,'user':user})

@login_required(login_url='login')
def ceoevent(request,pk):
 project = Project_DIP.objects.get(id=pk)
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
      plan = Event_Plan.objects.filter(is_submited = 1)
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
 return render(request,'myAPP/ceo-event.html', {'events': events,'project':project})

@login_required(login_url='login')
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
      return render(request,'myAPP/getdataEvent.html',{'data': form,'project':project}) 

@login_required(login_url='login')
def update_event(request,pk):
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
      return render(request,'myAPP/getdataEvent.html',{'data': form,'project':project}) 



@login_required(login_url='login')
def index4(request,pk):
    user=0
    if user_belongs_to_group(request.user,'ProjectManager'):
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
    return render(request,'myAPP/reporting-home.html', context)

@login_required(login_url='login')
def monthly_report(request,pk):
    user=0
    if user_belongs_to_group(request.user,'ProjectManager'):
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
      return render(request,'myAPP/achivment_form.html',{'form': form,'plan':plan,'project':project})

@login_required(login_url='login')
def add_report_highlights(request,pk):
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
      return render(request,'myAPP/highlights_form.html',{'form': form,'plan':plan,'project':project}) 

@login_required(login_url='login')
def add_report_backlog(request,pk):
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
      return render(request,'myAPP/backlog_form.html',{'form': form,'plan':plan,'project':project})  

@login_required(login_url='login')
def update_report(request,pk):
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
      return render(request,'myAPP/report-update.html',{'form': form,'plan':plan,'project':project}) 

@login_required(login_url='login')
@admin_only
def ceoreportapproval(request,pk):
    user=0
    if user_belongs_to_group(request.user,'ProjectManager'):
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
        form = ReportAproveForm(request.POST,instance=mp)
        if form.is_valid():
          data = form.save(commit=False)
          data.is_report_approved = True
          # data.is_report_submited = True
          data.is_report_rejected = False
          data.save()
      plan = Month_Plan.objects.filter(is_report_submited = 1)
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
        'Plans' : Plans,
        'month':month,
        'user': user
        }
    return render(request,'myAPP/ceo-report.html', context)

@login_required(login_url='login')
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
    if user_belongs_to_group(request.user,'ProjectManager'):
      user = 1
    else:
      user = 0
    project = get_object_or_404(Project_DIP, id=pk)
    month = datetime.today()
    Plans = Weekly_Report.objects.filter(activity_id__project_detail_id__project_id = project).filter(month=month.month).filter(year=month.year)
    context= {
        'project':project,
        'user': user,
        'Plans': Plans,
        'month': month,
        }
    return render(request,'myAPP/week-report.html', context)

@login_required(login_url='login')
def add_WeeklyReport(request,pk):
      project = get_object_or_404(Project_DIP, id=pk)
      form = WeeklyReportForm(pk=pk)
      context= {
          'form': form,
          'project':project,
          }
      return render(request,'myAPP/weekly-add.html',context) 

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

# @login_required(login_url='login')
# def week_remarks(request,pk):
#       plan = get_object_or_404(Weekly_Report, id=pk)
#       project = get_object_or_404(Project_DIP, id=plan.activity_id.project_detail_id.project_id.id)
#       form = WeekRemarkForm(instance=plan)
#       if request.method == 'POST':
#             form = WeekRemarkForm(request.POST,instance=plan)
#             if form.is_valid():
#                 form.save()
#                 return redirect('myAPP:weekly-report',project.pk)
#             else:
#                form = WeekRemarkForm(instance=plan)  
#       return render(request,'myAPP/event-remarks.html',{'form': form,'project':project})



@login_required(login_url='login')
def complince_home(request,pk):
  user=0
  if user_belongs_to_group(request.user,'ProjectManager'):
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
  return render(request,'myAPP/complince-home.html', context)

@login_required(login_url='login')
def add_project_clearance(request,pk):
  user=0
  if user_belongs_to_group(request.user,'ProjectManager'):
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
                return redirect('myAPP:complince-home', project.id)
            else:
               form = MPCForm()  
  context= {
        'project':project,
        'user': user,
        'form':form
  }
  return render(request,'myAPP/add-monthly-clearance.html', context)





# @login_required(login_url='login')
# def add_annual_budget(request):
#       form = annualBudgetForm()
#       if request.method == 'POST':
#             form = annualBudgetForm(request.POST)
#             if form.is_valid():
#                form.save()
#                messages.success(request,'Budget Created Successfully')
#             else:  # display empty form
#                form = annualBudgetForm()  
#       return render(request,'myAPP/addannualbudget.html',{'data': form}) 















