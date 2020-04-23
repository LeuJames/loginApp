from django.db import models
import re, bcrypt
from datetime import datetime

class userManager(models.Manager):

    def register_validator(self,postData):
        errors = {}
        if len(postData['f_name']) < 2:
            errors['f_name'] = "First name must be filled out and at least 2 characters long!"
        if len(postData['l_name']) < 2:
            errors['l_name'] = "Last name must be filled out and at least 2 characters long!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "Invalid email address!"
        elif len(User.objects.filter(email=postData['email'])) > 0:
            errors['existingEmail'] = "Email is already taken by another user"
        if postData['dob'] == '':
            errors['dob_empty'] = "Date of Birth must be filled out!"
        elif datetime.strptime(postData['dob'], "%Y-%m-%d") > datetime.now():
            errors['dob'] = "Date of birth must be in the past!"
        if len(postData['pw']) < 8:
            errors['pw'] = "Password must be at least 8 characters!"
        elif postData['pw'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Password does not match confirm password field!"
        return errors

    def login_validator(self,postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if len(user) < 1:
            errors['emailDoesNotExist'] = "Email does not exist"
        else:
            logged_user = user[0]
            if not bcrypt.checkpw(postData['pw'].encode(), logged_user.password.encode()):
                errors['badPW'] = "Password is incorrect!!"
        return errors

class User(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null = True)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()