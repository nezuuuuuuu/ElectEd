from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'dashboard_templates/dashboard_main.html')

def votes(request):
    return render(request, 'dashboard_templates/dashboard_votes.html')

def guidelines(request):
    return render(request, 'dashboard_templates/dashboard_guidelines.html')

def logout(request):
    #IMPLEMENT LOGOUT SA USER DIRI
    return