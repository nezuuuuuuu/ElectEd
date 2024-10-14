from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('votes/', views.votes, name='votes'),
    path('votes_candidates/<int:election_id>/', views.votes_candidates, name='votes_candidates'),  # Updated URL pattern
    path('guidelines/', views.guidelines, name='guidelines'),
]
