from django.shortcuts import render
import requests


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required
def get_user_info(request):
    user = request.user
    id = user.get_short_name().split(' ')[0]; 
    user_info = {
        'username': user.username,
        'email': user.email,
        'id' : id,
        'lastname' : user.last_name
        
       
    }
    return user_info

def main(request):
    return render(request, 'dashboard_templates/dashboard_main.html',get_user_info(request))

def votes(request):
    return render(request, 'dashboard_templates/dashboard_votes.html',get_user_info(request))

def guidelines(request):
    return render(request, 'dashboard_templates/dashboard_guidelines.html',get_user_info(request))

def logout(request):
    #IMPLEMENT LOGOUT SA USER DIRI
    return 