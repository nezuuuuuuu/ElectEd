from django.shortcuts import render, get_object_or_404
from .models import Election, Candidate, Position,Student, VoteSlip
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.db.models import Q 
import os # Import Q for complex queries
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json 
import logging

logger = logging.getLogger(__name__)



Logged_id=None

@login_required
def get_user_info(request):


    global Logged_id
    user = request.user
    id = {(user.get_short_name()).split(' ')[0]}
    Logged_id = str(id).replace('-', '').replace('{', '').replace('}', '').replace("'", '').replace('"', '').strip()
    # if(verif !=1):
    #     return
    print(Logged_id)
  
    initials=user.username.split('.')[0][0].upper()  + user.username.split('.')[1].split('@')[0][0].upper() 
    print(initials)
    if os.path.exists(f'static/initials/{initials}.jpg'):
        print('profile exist')
    else:

        create_profile_image(initials, f'{initials}.jpg')
    user_info = {
        'username': user.username,
        'email': user.email,
        'id' : id,
        'lastname' : user.last_name,
        'initials': initials,
        
    }
    return user_info


# def verif():
#      global Logged_id
#      for student in Student.objects:
#         student.student_id=Logged_id
#         return 1
#      return 0

def main(request):
    user_info=get_user_info(request)
    global Logged_id

    admins(request)
    return render(request, 'dashboard_templates/dashboard_main.html', {
        **get_user_info(request)  # Assuming this returns a dictionary
    })

def votes(request):
    user_info = get_user_info(request)
    global Logged_id

    student = get_object_or_404(Student, student_id=Logged_id)
    elections = Election.objects.filter(departments__contains=student.department)

    # Search functionality
    query = request.GET.get('q', '')
    if query:
        elections = elections.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )

    context = {
        'elections': elections,
    }
    context.update(user_info)
    return render(request, 'dashboard_templates/dashboard_votes.html', context)

def votes_candidates(request, election_id):
    
    election = get_object_or_404(Election, id=election_id)
    positions = Position.objects.filter(election=election)
    # candidates = Candidate.objects.filter(election=election).select_related('position')

# Get the search query from the request
    search_query = request.GET.get('q', '').strip()
    
    # Filter candidates based on the current election and search query
    if search_query:
        candidates = Candidate.objects.filter(
            election=election,
            name__icontains=search_query
        )
    else:
        candidates = Candidate.objects.filter(election=election)

    # Pass the filtered candidates, positions, and election to the template
    isDisabled= ''
   
    student=getStudentLoggedIn(request=request)
    try:
        if(VoteSlip.objects.get(student = student, election=election)):
            isDisabled= 'disabled'
    except Exception as e:
        isDisabled= ''    

    context = {
        'election': election,
        'positions': positions,
        'candidates': candidates,
        'disabled' : isDisabled
    }

    return render(request, 'dashboard_templates/dashboard_votes_candidates.html', context | get_user_info(request))


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
from .models import Student, Election, Candidate, VoteSlip
@csrf_exempt
@require_POST
def submit_votes(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)

        # Extract votes from the data
        votes = data.get('votes', [])
        ids=[]
        i=0
      
        election=None

        if not votes:
            # If no votes are provided, return an error response
            return JsonResponse({'success': False, 'error': 'No votes provided'})

        for vote in votes:
            candidate_id = vote.get('candidate_id')
            position = vote.get('position')

            # Check if candidate_id and position are present in each vote
            if not candidate_id:
                return JsonResponse({'success': False, 'error': 'Candidate ID missing in vote'})
            if not position:
                return JsonResponse({'success': False, 'error': 'Position missing in vote'})

            # Attempt to fetch the candidate from the database
            try:
                candidate = Candidate.objects.get(id=candidate_id)
            except Candidate.DoesNotExist:
                return JsonResponse({'success': False, 'error': f'Candidate with ID {candidate_id} not found'})
            ids.append(str(candidate_id))
            i+=1
            if(election==None):
                election=candidate.election
            # Increment the vote count for the selected candidate
        candidate.vote_count += 1
        candidate.save()
       
        print(candidate.election)
        student = getStudentLoggedIn(request=request) 
        voteslip = VoteSlip(student=student, election=election,candidates=ids)
           
           
             
            # voteslip.full_clean()  # Optional: Validate before saving
 
        voteslip.save()
        votes_candidates(request, candidate.election.id)
            


        # Return a success response if all votes were processed successfully
        return JsonResponse({'success': True})

    except json.JSONDecodeError:
        logger.error("Invalid JSON data")
        return JsonResponse({'success': False, 'error': 'Invalid JSON data in request'})
    
    except Exception as e:
        # Log any unexpected errors
        logger.error(f"Error submitting votes: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


from PIL import Image, ImageDraw, ImageFont

def create_profile_image(initials, output_path, size=256, text_color="white"):
 
    bg_color = (164, 28, 48)
    img = Image.new("RGB", (size, size), color=bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", int(size / 2))
    except IOError:
        font = ImageFont.load_default()


    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2.5


    draw.text((text_x, text_y), initials, fill=text_color, font=font)

    img.save(f'static/initials/{output_path}')
    print( output_path)


def getStudentLoggedIn(request):
    global Logged_id
    get_user_info(request=request)
    print(Logged_id)
   
    student = Student.objects.get(student_id=Logged_id)  
    return student
