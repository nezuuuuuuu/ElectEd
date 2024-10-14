from django.shortcuts import render, get_object_or_404
from .models import Election, Candidate, Position

# Create your views here.
def main(request):
    return render(request, 'dashboard_templates/dashboard_main.html')

def votes(request):
    elections = Election.objects.all()
    return render(request, 'dashboard_templates/dashboard_votes.html', {'elections': elections})

def votes_candidates(request, election_id):  # Accept election_id as a parameter
    election = get_object_or_404(Election, id=election_id)  
    positions = Position.objects.filter(election=election)  
    candidates = Candidate.objects.filter(election=election)    

    return render(request, 'dashboard_templates/dashboard_votes_candidates.html', {
        'positions': positions,
        'candidates': candidates,
        'election': election 
    })

def guidelines(request):
    return render(request, 'dashboard_templates/dashboard_guidelines.html')

def logout(request):
    # Implement logout functionality
    return


