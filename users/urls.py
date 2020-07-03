from django.urls import path
from . import views
urlpatterns = [
    path('signup',views.register),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('auth',views.auth_view,name="auth"),
    path('change-password',views.change_password,name="change-password"),
    path('reset-password',views.reset_password),
    path('forgot-password',views.forgot_password),
    path('edit-profile',views.view_update_user),
    path('profile',views.view_profile),
    path('feedback',views.feedback),
    path('delete-account',views.delete_user),
]