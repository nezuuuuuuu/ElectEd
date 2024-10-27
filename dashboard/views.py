from django.shortcuts import render, get_object_or_404
from .models import Election, Candidate, Position
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User


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
# Create your views here.
def main(request):
      user_info=get_user_info(request)
      admins(request)
      if request.user.is_authenticated and request.user.is_staff:
        return redirect('/admin/')       
            
      return render(request, 'dashboard_templates/dashboard_main.html',get_user_info(request))

def votes(request):
    elections = Election.objects.all()
    return render(request, 'dashboard_templates/dashboard_votes.html', {'elections': elections} |  get_user_info(request))


def votes_candidates(request, election_id):  # Accept election_id as a parameter
    election = get_object_or_404(Election, id=election_id)  
    positions = Position.objects.filter(election=election)  
    candidates = Candidate.objects.filter(election=election)    

    return render(request, 'dashboard_templates/dashboard_votes_candidates.html', {
        'positions': positions,
        'candidates': candidates,
        'election': election 
    })

def get_positions(request, election_id):
    positions = Position.objects.filter(election_id=election_id)
    positions_data = [{"id": position.id, "title": position.title} for position in positions]
    return JsonResponse({"positions": positions_data})

def guidelines(request):
    return render(request, 'dashboard_templates/dashboard_guidelines.html', get_user_info(request))

def logout(request):
    # Implement logout functionality
    return


def admins(request):
    try:
        user = User.objects.get(email="janedward.abadiano@cit.edu")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"User {user.email} is now an admin.")
    except User.DoesNotExist:
        print("User not found")