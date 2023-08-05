import datetime
import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

# Create your models here.
class Students(models.Model):
    roll = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    phone = models.CharField(max_length=12)
    
class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
class Inquiry(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    number = models.CharField(max_length=12)
    subject = models.CharField(max_length=80)
    
class Contact(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)

def filepaths(request, filename):
    filename = os.path.basename(filename)
    return os.path.join('media/',filename)


class AutoApplicationNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10  # You can adjust the length as needed
        kwargs['unique'] = True
        super(AutoApplicationNumberField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = get_random_string(10).upper()  # You can adjust the length as needed
        setattr(model_instance, self.attname, value)
        return value


class Allstudentsadmissionlist(models.Model):
    application_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    application_number_integer = models.BigIntegerField(editable=False, null=True)
    def save(self, *args, **kwargs):
        # Convert the UUID to an integer and set the application_number_integer field
        self.application_number_integer = int(str(self.application_number).replace('-', '')[:16], 16)
        super().save(*args, **kwargs)
    image =  models.ImageField(upload_to = filepaths, null=True, blank=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=10)
    fathername = models.CharField(max_length=12)
    mothername = models.CharField(max_length=100)
    Permanent_Address = models.CharField(max_length=250)
    country = models.CharField(max_length=12)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    Snumber = models.CharField(max_length=50)
    Gnumber = models.CharField(max_length=50)
    DOB = models.CharField(max_length=80)
    Religion = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    category = models.CharField(max_length=15)
    course = models.CharField(max_length=50)
    SSCyear = models.CharField(max_length=80)
    SSCBoard = models.CharField(max_length=50)
    t1 = models.CharField(max_length=100)
    m1 = models.CharField(max_length=50)
    p1 = models.CharField(max_length=50, null=True)
    HSCyear = models.CharField(max_length=80)
    HSCboard = models.CharField(max_length=50)
    t2 = models.CharField(max_length=10)
    m2 = models.CharField(max_length=10)
    p2 = models.CharField(max_length=10, null=True, blank=True)
    graduationYear = models.CharField(max_length=80)
    Collegename = models.CharField(max_length=12)
    t3 = models.CharField(max_length=100)
    m3 = models.CharField(max_length=50)
    p3 = models.CharField(max_length=50, null=True, blank=True)
    HSCstream = models.CharField(max_length=80)
   