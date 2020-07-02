from django.urls import path
from . import views
urlpatterns = [
    path('delete-container',views.getContainerDeletePage),
    path('viewfiles/<slug:eventname>',views.viewFiles),
    path('upload-files/<slug:eventname>',views.fileupload),
    path('base',views.home,name='base'),
    path('',views.home,name='base'),
    
]
