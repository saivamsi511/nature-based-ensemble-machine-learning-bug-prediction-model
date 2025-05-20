from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=3000)
    gender = models.CharField(max_length=300)


class bug_report_prediction(models.Model):

    bug_id= models.CharField(max_length=300)
    creation_date= models.CharField(max_length=300)
    component_name= models.CharField(max_length=300)
    product_name= models.CharField(max_length=300)
    short_description= models.CharField(max_length=3000)
    long_description= models.CharField(max_length=3000)
    reporter_name= models.CharField(max_length=300)
    resolution_category= models.CharField(max_length=300)
    status_category= models.CharField(max_length=300)
    bug_fix_time= models.CharField(max_length=300)
    Prediction= models.CharField(max_length=300)


class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



