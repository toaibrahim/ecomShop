from django.db import models

# Create your models here.

class Newletter(models.Model):
    email = models.EmailField()
    time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email
