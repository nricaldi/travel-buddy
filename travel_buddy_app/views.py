from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import datetime
import bcrypt


# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request, method="POST"):

    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        request.session['try'] = "register"
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    
    password = request.POST['password']
    hashed_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    new_user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashed_pass.decode())
    request.session['user_id'] = new_user.id

    return redirect("/travels")

def login(request, method="POST"):

    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        request.session['try'] = "login"
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")

    user = User.objects.filter(username=request.POST['username'])
    current_user = user[0]    
    request.session['user_id'] = current_user.id

    return redirect("/travels")

def travels(request):

    current_user = User.objects.get(id=request.session['user_id'])
    all_trips = Trip.objects.exclude(creator=current_user)

    all_trips = all_trips.exclude(passengers=current_user)
    
    context = {
        "user": current_user,
        "users_trips": current_user.joined_trips.all(),
        "all_trips": all_trips
    }

    return render(request, "travels.html", context)


def add_travel_plan(request):

    return render(request, "add_plan.html")

def add_trip(request, method="POST"):
    errors = Trip.objects.trip_validator(request.POST)
    print(Trip.objects.all())
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/add_travel_plan")

    user = User.objects.get(id=request.session['user_id'])
    new_trip = Trip.objects.create(creator=user, destination=request.POST['destination'], desc=request.POST['desc'], travel_date_from=request.POST['start_date'], travel_date_to=request.POST['end_date'])
    new_trip.passengers.add(user)

    return redirect("/travels")

def view_trip(request, trip_id):
    current_user = User.objects.get(id=request.session['user_id'])
    current_trip = Trip.objects.get(id=trip_id)

    context = {
        "trip": current_trip,
        "current_user": current_user,
        "other_users": current_trip.passengers.all()
    }

    return render(request, "view_trip.html", context)

def join_trip(request, trip_id):
    current_user = User.objects.get(id=request.session['user_id'])
    current_trip = Trip.objects.get(id=trip_id)

    current_trip.passengers.add(current_user)


    return redirect("/travels")


def logout(request):
    request.session.clear()
    return redirect("/")