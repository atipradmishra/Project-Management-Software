from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myAPP.views import loginPage, logoutUser



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginPage,name='login'),
    path('logout/', logoutUser,name='logout'),
    path('ycda/', include('myAPP.urls','myAPP'), name="myAPP"),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    




