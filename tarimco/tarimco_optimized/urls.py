from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from myapp.views import CustomLoginView
from myapp.forms import LoginForm
from django.urls import path, include,re_path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='registration/girisyap.html' ,authentication_form=LoginForm), name='login'),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
]   
