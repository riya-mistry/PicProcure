from django.urls import path
from . import views
urlpatterns = [
    path('uploaded',views.uploaded,name="uploaded"),
    path('demo',views.demoupload),
    path('',views.index,name='index'),
    
]
