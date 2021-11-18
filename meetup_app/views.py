from django.shortcuts import render, redirect
from .models import *
import bcrypt
import datetime as dt
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'login.html')

def user_create(request):
    if request.method == "POST":
        errors = User.objects.reg_valid(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(
                name = request.POST['name'],
                email = request.POST['email'],
                b_day = request.POST["b_day"],
                password = pw_hash,
            )
            request.session["user_id"] = new_user.id
            return redirect('/dashboard')
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')
    else:
    #get ID and display info
        one_user = User.objects.get(id=request.session['user_id'])
        event_list = Event.objects.all().order_by("-created_at")
        context = {
            'user': one_user,
            'all_events': event_list,
            # 'attendees': Event.objects.filter('attending'),
        }
        return render(request, 'dashboard.html', context)

def logout(request):
    request.session.flush()
    return redirect("/")

def login(request):
    if request.method == "POST":
        errors = User.objects.login_valid(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        else:
            user = User.objects.get(email=request.POST['l_email']) 
            if bcrypt.checkpw(request.POST['l_password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
            return redirect('/dashboard')
    return redirect('/')

def user_profile(request, user_id):
    if 'user_id' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')
    else:
        one_user = User.objects.get(id=request.session['user_id'])
        type_choices = User.type_choices
        # this_users_events: Event.objects.filter(user_creater=one_user).order_by("-created_at")
        # User.objects.get(user_events).order_by("-created_at")
        context = {
            'user' : one_user,
            'type_choices': type_choices,
            'all_users_events': Event.objects.filter(attending=one_user).order_by("-created_at"),
        }
    return render(request, 'user_profile.html', context)

def update_user(request, user_id):
    if request.method == 'POST':
        errors = User.objects.user_update_valid(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/profile/{user_id}')
        else:
            update_user = User.objects.get(id=user_id)
            update_user.name = request.POST['name']
            update_user.email = request.POST['email']
            update_user.player_type = request.POST['type_dropdown']
            update_user.save()
            return redirect(f'/profile/{user_id}')
    return redirect('/')

def update_user_about(request, user_id):
    if request.method == 'POST':
        update_user = User.objects.get(id=user_id)
        update_user.about_me = request.POST['about_me']
        update_user.save()
        return redirect(f'/profile/{user_id}')
    return redirect('/')

# EVENTS
def plan_event(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else: 
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user' : User.objects.get(id=request.session['user_id']),
        }
    return render(request, 'event_create.html', context)

def add_event(request):
    if request.method == "POST":
        errors = Event.objects.event_valid(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/add_event')
        else:
            this_user = User.objects.get(id=request.session['user_id'])
            this_event = Event.objects.create(
                title = request.POST['title'],
                event_date = request.POST['event_date'],
                time = request.POST['time'],
                address = request.POST['address'],
                city = request.POST['city'],
                details = request.POST['details'],
                user_creater = this_user,
            )
            this_event.attending.add(this_user)
            return redirect('/dashboard')
    return redirect('/login')

# def info_event(request, event_id):
#     if 'user_id' not in request.session:
#         return redirect('/')
#     else: 
#         user = User.objects.get(id=request.session['user_id'])
#         context = {
#             'user' : User.objects.get(id=request.session['user_id']),
#         }
#     return render(request, 'event_edit.html', context)

def event(request, event_id):
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'event': event,
        'user' : user,
        # 'attending_list' : Event.objects.exclude(attending=user)
    }
    if event.user_creater.id == user.id:
        return render(request, 'event_edit.html', context)

    else:
        return render(request, 'event_show.html', context)

def edit_event(request, event_id):
    errors = Event.objects.event_edit_valid(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit_event/{event_id}')
    else:
        this_event = Event.objects.get(id=event_id)
        user = User.objects.get(id=request.session['user_id'])
        this_event.title = request.POST['title']
        this_event.address = request.POST['address']
        this_event.city = request.POST['city']
        this_event.details = request.POST['details']
        this_event.save()
        return redirect(f'/profile/{user.id}')
        # event_date = request.POST['event_date']
        # time = request.POST['time']

def delete_event (request, event_id):
    this_event = Event.objects.get(id=event_id)
    this_event.delete()
    return redirect('/dashboard')

def attending(request, user_id, event_id):
    event = Event.objects.get(id=event_id)
    one_user = User.objects.get(id=request.session['user_id'])
    event.attending.add(one_user)
    event.save()
    return redirect(f'/event/{event_id}')

def not_attending(request, user_id, event_id):
    event = Event.objects.get(id=event_id)
    one_user = User.objects.get(id=request.session['user_id'])
    event.attending.remove(one_user)
    event.save()
    return redirect(f'/event/{event_id}')

# def change_pass(request, user_id):
#     password = request.POST['password']
#     pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
#     password = pw_hash
#     user_id.password = request.POST['password']
