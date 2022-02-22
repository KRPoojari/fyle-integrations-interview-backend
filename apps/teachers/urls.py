from django.urls import path
from apps.teachers.views import TeachersView

urlpatterns = [
     path('assignments/', TeachersView.as_view(), name='teachers-assignments')
]

