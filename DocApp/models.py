from http.client import NotConnected
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='files', height_field=None, width_field=None, max_length=None)
    spec = models.CharField(max_length=50)
    best = models.BooleanField(default=False)



class NewAppointment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,)
    date = models.DateTimeField()
    time = models.TimeField()

class NewReview(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,)
    comment = models.TextField(blank=True, null=True)
    rate = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    


def __str__(self):
    return str(self.id)

