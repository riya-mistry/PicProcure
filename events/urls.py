from django.urls import path
from . import views
urlpatterns = [
    path('generate-event',views.new_event),
]