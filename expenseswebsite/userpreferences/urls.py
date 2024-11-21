from django.urls import path
from . import views

urlpatterns = [
    path('preferences/', views.index, name='preferences'),
   
]