from django.urls import path
from . import views
urlpatterns = [
    path('signup',views.register),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('auth',views.auth_view,name="auth"),
    path('feedback',views.feedback,),
]