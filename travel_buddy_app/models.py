from django.db import models
import datetime
import bcrypt

# Create your models here.\
class User_Manager(models.Manager):
    def registration_validator(self, postData):
        errors = {}

        if len(postData['name']) < 1 and len(postData['username']) < 1 and len(postData['password']) < 1 and len(postData['confirm']) < 1:
            errors['form'] = "Please fill out form"
            return errors
        else:
            if len(postData['name']) < 3:
                errors['name'] = "Name should be at least 3 characters"
            if len(postData['username']) < 3:
                errors['username'] = "Username should be at least 3 characters"
            user = User.objects.filter(username=postData['username'])
            if user:
                errors['username'] = "Username already in use"
            if len(postData['password']) < 8: 
                errors['password'] = "Password should be at least 8 characters"
            else:
                if postData['password'] != postData['confirm']:
                    errors['confirm'] = "Passwords do not match"

        return errors

    def login_validator(self, postData):
        errors = {}

        if len(postData['username']) < 1 and len(postData['password']) < 1: 
            errors['form'] = "Please fill out form"
            return errors
        else:
            user = User.objects.filter(username=postData['username'])
            if not user: 
                errors['username'] = "Not a registered user"
            else: 
                current_user = user[0]
                if not (bcrypt.checkpw(postData['password'].encode(), current_user.password.encode())):
                    errors['password'] = "Incorrect Password"
    
        return errors

class Trip_Manager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 1 and len(postData['desc']) < 1 and len(postData['start_date']) < 1 and len(postData['end_date']) < 1:
            errors["form"] = "Please fill out form"
            return errors
        else:
            if len(postData['destination']) < 1:
                errors['destination'] = "Please fill out destination"
            if len(postData['desc']) < 1: 
                errors["desc"] = "Please fill out description"
            if len(postData['start_date']) < 1:
                errors['start_date'] = "Please enter a start date"
            if len(postData['end_date']) < 1:
                errors['start_date'] = "Please enter an end date"
            start = postData['start_date'] 
            end = postData['end_date']
            now = str(datetime.datetime.now())
            if start < now:
                errors['start_date'] = "Start date cannot be in the past"
            if end < start:
                errors['end_date'] = "End cannot be before the start"
        return errors
        
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_Manager()

class Trip(models.Model):
    creator = models.ForeignKey(User, related_name="created_trips", on_delete=models.CASCADE)
    passengers = models.ManyToManyField(User, related_name="joined_trips")
    destination = models.CharField(max_length=255)
    desc = models.TextField()
    travel_date_from = models.DateTimeField()
    travel_date_to = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Trip_Manager()