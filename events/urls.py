from django.urls import path
from . import views
urlpatterns = [
    path('generate-event',views.new_event),
    path('download-zip/<slug:eventname>/',views.combine),
    path('cluster/<slug:eventname>/',views.cluster),
    path('download-img/<slug:eventname>/<str:blobname>',views.stream_file),
    path('register/<slug:eventname>/',views.register),
    path('view-events',views.viewEvents),
    path('my-events',views.my_events),
    path('remove-user/<slug:eventname>/<str:user_id>',views.remove_user),
    path('registered-events/',views.registered),
   
]