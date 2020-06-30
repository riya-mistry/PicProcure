from django.urls import path
from . import views
urlpatterns = [
    path('generate-event',views.new_event),
    path('demo',views.combine),
    path('cluster',views.cluster),
    path('download',views.stream_file),
]