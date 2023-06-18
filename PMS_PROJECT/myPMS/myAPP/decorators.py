from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Group


def user_belongs_to_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False
    return user.groups.filter(name=group_name).exists()

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			if user_belongs_to_group(request.user,'CEO'):
				return redirect('myAPP:masterhome')
			else:
				return redirect('myAPP:logout')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'ProjectManager':
			return redirect('myAPP:login')

		if group == 'CEO':
			return view_func(request, *args, **kwargs)

	return wrapper_function