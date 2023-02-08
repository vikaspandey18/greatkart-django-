from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register,name='register'),
    path('login/', views.login_user,name='login'),
    path('logout/', views.logout_user,name='logout'),
    path('activate/<uidb64>/<token>/', views.activate,name='activate'),
    path('dashboard', views.dashboard,name='dashboard'),
    path('', views.dashboard,name='dashboard'),
    path('forgetpassword/', views.forgetpassword,name='forgetpassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword/', views.resetpassword,name='resetpassword'),
]
