from django.db import models

class Photo(models.Model):
    image = models.ImageField(upload_to='uploads')
    description = models.CharField(max_length=50)


    def __str__(self):
        return self.description

class PhotoPost(models.Model):
    image = models.ImageField(upload_to='uploads/posts')