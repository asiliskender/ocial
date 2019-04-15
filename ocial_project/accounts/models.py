from django.db import models
from django.contrib.auth.models import User


class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ManyToManyField('topics.Course', blank=True)
