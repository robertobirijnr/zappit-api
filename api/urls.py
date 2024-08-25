from django.urls import path
from . import views

urlpatterns = [
     path('todos/complete', views.TodoCompletedList.as_view()),
]
