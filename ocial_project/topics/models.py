from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class Topic(models.Model):
	title = models.CharField(max_length=200,unique=True)

	def __str__(self):
		return self.title


class Course(models.Model):
	title = models.CharField(max_length=200)
	pubdate = models. DateTimeField()
	image = models.ImageField(upload_to='images/', default= '../static/default.jpg')
	description = models.TextField(blank=True)
	wywl = models.TextField(blank=True)
	teacher = models.ForeignKey(User, on_delete=models.CASCADE)
	topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
	label = models.ManyToManyField('Label', blank=True)
	published = models.BooleanField(default=False)


	def pub_date_exact(self):
		return self.pubdate.strftime('%e %B %Y %H:%M')


	def pub_date(self):
		return self.pubdate.strftime('%e %B %Y')

	def __str__(self):
		return self.title

	def summary(self):
		return self.description[:200]

class Label(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return self.name

class Glossary(models.Model):
	name = models.CharField(max_length=200)
	image_url = models.CharField(max_length=1000, blank=True)
	description = models.TextField(blank=True)
	url = models.CharField(max_length=1000, blank=True)
	course = models.ForeignKey('Course', on_delete=models.CASCADE)


	def __str__(self):
		return self.name

class Section(models.Model):
	name = models.CharField(max_length=200)
	course = models.ForeignKey('Course', on_delete=models.CASCADE)
	order =  models.IntegerField(default=1)
	description = models.TextField(blank=True)


	class Meta:
		ordering = ['order']

	def __str__(self):
		return self.name

class Lecture(models.Model):
	title = models.CharField(max_length=200)
	body = models.TextField(blank=True)
	section = models.ForeignKey('Section', on_delete=models.CASCADE)
	order =  models.IntegerField(default=1)

	class Meta:
		ordering = ['order']
		verbose_name = 'Lecture'

	def __str__(self):
		return self.title

class Quiz(models.Model):
	title = models.CharField(max_length=200)
	section = models.ForeignKey('Section', on_delete=models.CASCADE)
	order =  models.IntegerField(default=1)
	successrate =  models.IntegerField(default=0)


	class Meta:
		ordering = ['order']
		verbose_name = 'Quiz'

	def __str__(self):
		return self.title

class Question(models.Model):
	title = models.TextField(blank=True)
	quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
	order =  models.IntegerField(default=1)

	class Meta:
		ordering = ['order']
		verbose_name = 'Question'

	def __str__(self):
		return self.title

class Choice(models.Model):
	title = models.TextField(blank=True)
	question = models.ForeignKey('Question', on_delete=models.CASCADE)
	order =  models.IntegerField(default=1)
	isTrue = models.BooleanField(default=False)


	class Meta:
		ordering = ['order']
		verbose_name = 'Choice'

	def __str__(self):
		return self.title

class Resource(models.Model):
	name = models.CharField(max_length=200, blank=True)
	link = models.FileField(upload_to='sources/', blank=True)
	section = models.ForeignKey('Section', on_delete=models.CASCADE)


	def __str__(self):
		return self.name
