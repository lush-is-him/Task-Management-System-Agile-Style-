from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task ,Team
from .forms import TaskForm



# User Login
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have logged in successfully!")
                return redirect('dashboard')  # Redirect to dashboard after login

            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Form is invalid. Check your credentials.")  # Debugging line
    
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form}) 


# User Logout
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


# User Registration
def user_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')  # 🔹 Redirect to login after successful registration
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})  


# authentication/views.py

from django.shortcuts import render
from .models import Task, Team

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Optional: redirect if user not logged in

    teams = Team.objects.filter(members=request.user)
    tasks_by_team = {}

    for team in teams:
        tasks_by_team[team.name] = Task.objects.filter(team=team)

    tasks_by_team["Personal Tasks"] = Task.objects.filter(assigned_to=request.user, team__isnull=True)

    print(tasks_by_team)  # what's inside the dictionary just to test


    return render(request, 'authentication/dashboard.html', {
        'tasks_by_team': tasks_by_team,
        'user': request.user
    })


@login_required
def add_task(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'M')
        team_id = request.POST.get('team')

        team = Team.objects.get(id=team_id) if team_id else None

        Task.objects.create(
            name=name,
            description=description,
            priority=priority,
            assigned_to=request.user,
            team=team
        )
        return redirect('dashboard')

    user_teams = request.user.teams.all()
    return render(request, 'authentication/add_task.html', {'user_teams': user_teams})



def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('dashboard')  # Redirect back to the dashboard


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.name = request.POST.get('name')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')
        task.priority = request.POST.get('priority')
        task.save()
        return redirect('dashboard')
    
    return render(request, 'authentication/update_task.html', {'task': task})



@login_required
def create_team(request):
    if request.method == 'POST':
        team_name = request.POST.get('name')
        if team_name:
            team = Team.objects.create(name=team_name, leader=request.user)
            team.members.add(request.user)  # Optional: Add leader as a member too
            return redirect('dashboard')
    return render(request, 'authentication/create_team.html')

@login_required
def view_team_members(request, team_id):
    team = Team.objects.get(id=team_id)
    if request.user not in team.members.all():
        return HttpResponseForbidden("You're not a member of this team.")

    members = team.members.all()
    return render(request, 'authentication/view_members.html', {'team': team, 'members': members})

@login_required
def edit_team(request, team_id):
    team = get_object_or_404(Team, id=team_id, leader=request.user)
    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name:
            team.name = new_name
            team.save()
            return redirect('dashboard')
    return render(request, 'authentication/edit_team.html', {'team': team})

@login_required
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id, leader=request.user)
    team.delete()
    return redirect('dashboard')

@login_required
def add_member(request, team_id):
    team = get_object_or_404(Team, id=team_id, leader=request.user)
    users = User.objects.exclude(id__in=team.members.all()).exclude(id=team.leader.id)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        team.members.add(user)
        return redirect('dashboard')

    return render(request, 'authentication/add_member.html', {'team': team, 'users': users})

