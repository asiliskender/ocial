from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import *
from django.db.models import Count
import operator



def home(request):
	topics = Topic.objects.annotate(number_of_answers=Count('course')) 
	topics = sorted(topics, key=operator.attrgetter('number_of_answers'),reverse=True)
	topics = topics[:9]
	return render(request, 'topics/home.html', {'topics': topics })

def topics(request):
	if request.method == 'GET': # If the form is submitted
		search_query = request.GET.get('search_topic', None)

		if search_query != None:
			topics = Topic.objects.filter(title__icontains=search_query).annotate(number_of_answers=Count('course')) 
		else:
			topics = Topic.objects.annotate(number_of_answers=Count('course')) 
			topics = sorted(topics, key=operator.attrgetter('number_of_answers'),reverse=True)
		
		return render(request, 'topics/topics.html', {'topics': topics})


def courses(request):
	if request.method == 'GET': # If the form is submitted
		search_query = request.GET.get('search_course', None)

		if search_query != None:
			courses = Course.objects.filter(title__icontains=search_query)
		else:
			courses = Course.objects.all()
			#courses = sorted(courses,reverse=True)
		
		return render(request, 'topics/courses.html', {'courses': courses})


@login_required
def classroom(request):
	courses = Course.objects.filter(teacher=request.user)
	return render(request, 'topics/classroom.html',{'courses': courses })

@login_required
def teacher(request):
	courses = Course.objects.filter(teacher=request.user)
	return render(request, 'topics/teacher.html',{'courses': courses })


@login_required
def newcourse(request):
	topics = Topic.objects.all()
	if request.method == 'POST':
		if request.POST['title'] and request.POST.getlist('topic'):
			course = Course()
			course.title = request.POST['title']
			course.description = request.POST['description']
			course.wywl = request.POST['wywl']
			course.pubdate = timezone.datetime.now()
			course.teacher = request.user

			topic_title = request.POST.get('topic')
			course.topic  = Topic.objects.get(id=topic_title)
		

			if request.FILES.get('image', False):
				course.image = request.FILES['image']

			labels = request.POST['labels']
			labels = labels.split(",")

			course.save()

			if request.POST['labels']:
				for label in labels:
					newlabel , created = Label.objects.get_or_create(name = label)
					course.label.add(newlabel)

			return redirect('teacher')
			#return render(request, 'topics/newcourse.html', {'topics': topics , 'error': labels})	

		else:
			return render(request, 'topics/newcourse.html', {'topics': topics , 'error': 'Title and Topic fields are required'})	
	else:
		return render(request, 'topics/newcourse.html',{'topics': topics})









