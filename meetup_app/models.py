from django.db import models
import re
import datetime as dt

from django.db.models.fields import EmailField

import bcrypt

# Create your models here.

class UserManager(models.Manager):
    def reg_valid(self, postData):
        errors = {}

        if len(postData['name']) < 2:
            errors["name"] = "Please enter a valid name. Must be at least 2 characters"
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0 or not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address"
        email_exists = self.filter(email=postData['email'])
        if email_exists:
            errors['duplicate'] = "Email already exists."

        if len(postData["b_day"]) > 0:
            date_entered = dt.datetime.strptime(postData["b_day"], "%Y-%m-%d")
            if date_entered > dt.datetime.now():
                errors["birthday"] = 'Please enter a valid birthday'
        
        PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,}$')
        if not PASSWORD_REGEX.match(postData['password']):
            errors["password"] = "Password must be a minimum of five characters with at least one letter and one number"
        if postData["password"] != postData["confirm"]:
            errors["match"] = "Passwords did not match"
        
        return errors
    
    def login_valid(self, postData):
        errors = {}
        if len(postData['l_password']) < 5:
            errors["l_password"] = "Password is not valid"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['l_email']) == 0 or not EMAIL_REGEX.match(postData['l_email']):            
            errors['email'] = "Invalid email address"
        email_exists = self.filter(email=postData['l_email'])
        if not email_exists:
            errors['email'] = "Email not Registered."
        else: 
            user = User.objects.get(email=postData['l_email'])
            if not bcrypt.checkpw(postData['l_password'].encode(), user.password.encode()):
                errors["password"] = "Incorrect password"
        return errors
        
    def user_update_valid(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "Please enter a valid name. Must be at least 2 characters"
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0 or not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address"

        # if len(postData["b_day"]) > 0:
        #     date_entered = dt.datetime.strptime(postData["b_day"], "%Y-%m-%d")
        #     if date_entered > dt.datetime.now():
        #         errors["birthday"] = 'Please enter a valid birthday'
        return errors

class GameManager(models.Manager):
    def game_valid(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors["title"] = "Please enter a valid title. Must be at least 2 characters"

        # NEED a URLValidator?

        # def checkURL(value):
        #     # check if valid URL
        #     pass
        return errors

class GameTypeManager(models.Manager):
    def type_valid(self, postData):
        errors = {}
        if len(postData['types']) < 2:
            errors["types"] = "Please enter a valid type. Must be at least 2 characters"
        type_exist = GameType.objects.filter(types=postData['types'])
        if len(type_exist) >= 1:
            errors["duplicate"] = "Type already exists"
        return errors

class EventManager(models.Manager):
    def event_valid(self, postData):
        errors = {}

        if len(postData['title']) > 50:
            errors["title"] = "Title must be less than 50 characters"
        
        if len(postData["event_date"]) > 0:
            date_entered = postData["event_date"]
            event_date = dt.datetime.strptime(date_entered, '%Y-%m-%d')

        if event_date < dt.datetime.now():
            errors["event_date"] = 'Event Date should be in the future'

        if len(postData['details']) < 5:
            errors["details"] = "Details should be at least 5 characters"
        return errors

    def event_edit_valid(self, postData):
        errors = {}

        if len(postData['title']) > 50:
            errors["title"] = "Title must be less than 50 characters"

        if len(postData['details']) < 5:
            errors["details"] = "Details should be at least 5 characters"
        return errors

class User(models.Model):
    type_choices = [
        ("I've Played Some Monopoly Before", "I've Played Some Monopoly Before"),
        ("I've Played Cards Against Humanity", "I've Played Cards Against Humanity"),
        ("I enjoy Playing Games with Friends", "I enjoy Playing Games with Friends"),
        ("I Own Gloomhaven!", "I Own Gloomhaven!"),
        ("Don't Bend the Cards!!", "Don't Bend the Cards!!"),
        ("Now I Just Need to Sleeve Everything...", "Now I Just Need to Sleeve Everything..."),
        ("Wow...I've spent Too Much", "Wow...I've spent Too Much"),
        ("Superbacker on Kickstarter", "Superbacker on Kickstarter"),
        ("Lord to Cardboard", "Lord to Cardboard"),
    ]
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=255)
    b_day = models.DateField()
    about_me = models.TextField(blank=True)
    player_type = models.CharField(max_length=45, choices=type_choices, blank=True)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # fav_games = []
    # user_events[]
    # groups mtm (create a group model "models.group" with name and permissions)

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    buy_link = models.URLField(max_length = 200, blank=True)
    rules_link = models.URLField(max_length = 200, blank=True)
    user_favs = models.ManyToManyField(User, related_name='fav_games')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GameManager()
    # types = []
    # many to many with events

class GameType(models.Model):
    type = models.CharField(max_length=45)
    games = models.ManyToManyField(Game, related_name="types")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GameTypeManager()

class Event(models.Model):
    title = models.CharField(max_length=50)
    event_date = models.DateField()
    time = models.TimeField()
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    details = models.TextField()
    user_creater = models.ForeignKey(User, related_name="user_events", on_delete=models.CASCADE)
    attending = models.ManyToManyField(User, related_name='user_attending') # add user_creater to list in the function automactically
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()
# each event can have many games


# FAVORITE OR RATING/REVIEW
# class ReviewMananger(models.Manager):
    # def review_valid(self, postData):
    #     errors = {}
    #     if len(postData['content']) < 8:
    #         errors["content"] = "Please enter a review of at least 8 characters"
    #     return errors
# class Review(models.Model):
    # content = models.TextField()
    # rating = models.IntegerField()
    # user_review = models.ForeignKey(User, related_name="user_reviews", on_delete=models.CASCADE)
    # game_reviewed = models.ForeignKey(Book, related_name="game_reviewed", on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # objects = ReviewMananger()

# MESSAGE BOARD
# class Message(models.Model):
#     message = models.TextField()
#     user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
# class Comment(models.Model):
#     comment = models.TextField()
#     user = models.ForeignKey(User)
#     message = models.ForeignKey(Message, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# USER MESSAGE
# class UserMessage(models.Model):
#     message = models.TextField()
#     user_to = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
#     user_from = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)