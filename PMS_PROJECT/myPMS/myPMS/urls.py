from django.contrib import admin
from django.urls import path, include

from myAPP.views import loginPage, logoutUser



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginPage,name='login'),
    path('logout/', logoutUser,name='logout'),
    path('ycda/', include('myAPP.urls','myAPP'), name="myAPP"),

    

]




    




