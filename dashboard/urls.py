from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('votes/', views.votes, name='votes'),
    path('guidelines/', views.guidelines, name='guidelines')
]