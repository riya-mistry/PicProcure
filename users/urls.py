from django.urls import path
from . import views
urlpatterns = [
    path('signup',views.register),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('auth',views.auth_view,name="auth"),
<<<<<<< HEAD
    path('change-password',views.change_password,name="change-password"),
    path('reset-password',views.reset_password),
    path('forgot-password',views.forgot_password),
    path('profile',views.view_update_user),
=======
    path('feedback',views.feedback,),
>>>>>>> faf04c06a4dcdb0fe212c22db06ab380c9c4556f
]