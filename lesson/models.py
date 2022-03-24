from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Team(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique_for_date='publish')

    body = models.TextField()

    cover = models.ImageField(upload_to='images/')

    created  = models.DateField(auto_now_add=True)
    updeted  = models.DateField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_teams')

    publish = models.DateTimeField(default=timezone.now())

    TEAM_TYPE = [
        ('группа A', 'Группа А в НБЛ'),
        ('группа B', 'Группа В в НБЛ'),
    ]

    team_type = models.CharField(max_length=25, choices=TEAM_TYPE, default='руппа А')

    # def __str__(self):
    #     return self.title

    def get_absolute_url(self):
        return reverse('lesson:detailed_team',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    team = models.ForeignKey(Team,
                                 on_delete=models.CASCADE,
                                 related_name='comments')
    name = models.CharField(max_length=250)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth = models.DateTimeField(null=True, blank=True)
    photo = models.ImageField(upload_to="user/%Y/%m/%d/", blank=True)