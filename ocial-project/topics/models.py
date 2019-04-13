from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
	title = models.CharField(max_length=200,unique=True)
	courses_total = models.IntegerField(default = 0)

	def __str__(self):
		return self.title


class Course(models.Model):
	title = models.CharField(max_length=200)
	pubdate = models. DateTimeField()
	image = models.ImageField(upload_to='images/', default='static/default.jpg')
	description = models.TextField(blank=True)
	teacher = models.ForeignKey(User, on_delete=models.CASCADE)
	topic = models.ForeignKey('Topic', on_delete=models.CASCADE)

	def pub_date(self):
		return self.pubdate.strftime('%b %e %Y')

	def __str__(self):
		return self.title

	def summary(self):
		return self.description[:150]