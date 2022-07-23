from distutils.command.upload import upload
from email.policy import default
from wsgiref.simple_server import demo_app
from django.db import models

# Create your models here.


from django.contrib.auth.models import User

class Album(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     title=models.CharField(max_length=100,default='General')
     

     def __str__(self):
          return self.title


class Photo(models.Model):
     category=models.ForeignKey(Album,on_delete=models.CASCADE)
     title=models.CharField(max_length=100,default='User Image')
     description=models.TextField(default="My New Image")
     image=models.ImageField(upload_to='images',default='')


     def __str__(self):
          return self.title
