from django.contrib import admin
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logoutView, name='logout'),
    path('sss/', views.sss, name='sss'),
    path('politika/', views.politika, name='politika'),
    path('sozlesme/', views.sozlesme, name='sozlesme'),
    
    path('market/', views.market, name='market'),
    path('urunekle/', views.urun_ekle, name='urun_ekle'),
    path('urun/<int:urun_id>/', views.urun_detay, name='urun_detay'),
    path('search/', views.search, name='search'),
    
    path('iletisim/', views.iletisim , name='iletisim'),
    
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('user/<int:user_id>/like/', views.like_user, name='like_user'),
    path('user/<int:user_id>/dislike/', views.dislike_user, name='dislike_user'),
    
    path('user/<int:user_id>/comment/', views.add_comment, name='add_comment'),
    path('user/<int:user_id>/comment/<int:parent_id>/', views.add_comment, name='add_reply'),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
