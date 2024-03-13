from import_export import resources
from django.contrib.auth.models import User
from .models import Profile, Project_DIP

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'first_name', 'last_name','groups')
        export_order = ('id','username', 'email', 'first_name', 'last_name','groups')
class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile
        fields = ('id','user', 'gender', 'designation', 'address','phone_no')
        export_order = ('id','user', 'gender', 'designation', 'address','phone_no')
class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project_DIP
        fields = ('id','project_name', 'category_id', 'assigned_to', 'budget','start_date','end_date', 'period','donor_name')
        export_order = ('id','project_name', 'category_id', 'assigned_to', 'budget','start_date','end_date', 'period','donor_name')