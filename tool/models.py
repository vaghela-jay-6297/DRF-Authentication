from django.db import models


# Create your models here.
class Tool(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default='None')
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
