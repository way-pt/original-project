from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


fsI = FileSystemStorage(location="media/")
fsT = FileSystemStorage(location="media/")
# Create your models here.

class Map(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, to_field='username')
    data = models.FileField(upload_to="dataFiles")
    image = models.ImageField(upload_to="photos", null=True, blank=True)
    name = models.CharField(max_length=50, help_text="A name for the map.", null=True, blank=True)

    # def __str__(self):
        
    #     return f'[{self.user.get_username()}] {self.name}'
