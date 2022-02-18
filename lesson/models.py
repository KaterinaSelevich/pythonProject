from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Material(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255)

    body = models.TextField()

    created  = models.DateField(auto_now_add=True)
    updeted  = models.DateField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_materials')

    publish = models.DateTimeField(default=timezone.now())

    MATERIAL_TYPE = [
        ('theory', 'theoretical material'),
        ('practice', 'Practical Task'),
    ]

    material_type = models.CharField(max_length=25, choices=MATERIAL_TYPE, default='theory')

    def __str__(self):
        return self.title
