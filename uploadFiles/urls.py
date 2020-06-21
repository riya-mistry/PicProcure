from django.urls import path
from . import views
urlpatterns = [
    path('delete-container',views.getContainerDeletePage),
    path('viewfiles',views.viewFiles),
    path('uploaded',views.uploaded,name="uploaded"),
    path('demo',views.demoupload),
    path('base',views.home,name='base'),
    path('',views.home,name='base'),
    
]
