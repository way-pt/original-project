from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


fsI = FileSystemStorage(location="/media/photos")
fsT = FileSystemStorage(location="media/dataFiles")
# Create your models here.

class Map(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    data = models.FileField(upload_to="media/dataFiles", storage=fsT)
    image = models.ImageField(storage=fsI, upload_to="media/photos", null=True, blank=True)
    
