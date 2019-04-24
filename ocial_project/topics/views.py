from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import *
from django.db.models import Count
import operator
import requests
import json
from wikidata.client import Client



def home(request):
	topics = Topic.objects.annotate(number_of_courses=Count('course')) 
	topics = sorted(topics, key=operator.attrgetter('number_of_courses'),reverse=True)
	topics = topics[:9]
	return render(request, 'topics/home.html', {'topics': topics })

def topics(request):
	if request.method == 'GET': # If the form is submitted
		search_query = request.GET.get('search_topic', None)

		if search_query != None:
			topics = Topic.objects.filter(title__icontains=search_query).annotate(number_of_courses=Count('course')) 
		else:
			topics = Topic.objects.annotate(number_of_courses=Count('course')) 
			topics = sorted(topics, key=operator.attrgetter('number_of_courses'),reverse=True)
		
		return render(request, 'topics/topics.html', {'topics': topics})

def explore(request):
	if request.method == 'GET': # If the form is submitted
		search_query = request.GET.get('search_course', None)
		search_query_topic = request.GET.get('search_topic', None)

		if search_query != None:
			courses = Course.objects.filter(title__icontains=search_query, published=True)
		elif search_query_topic != None:
			courses = Course.objects.filter(topic=search_query_topic, published=True)
		else:
			courses = Course.objects.filter(published=True)
			#courses = sorted(courses,reverse=True)
		
		return render(request, 'topics/explore.html', {'courses': courses})

def coursedetail(request, course_id):
	course =  get_object_or_404(Course,pk=course_id, published=True)
	return render(request, 'topics/course_detail.html', {'course': course})



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
		if 'newtopic' in request.POST:
			topic , created = Topic.objects.get_or_create(title=request.POST['topictitle'])
			topic.save()
			return redirect('newcourse')
		if 'save' in request.POST:
			if request.POST['title'] and request.POST.getlist('topic'):
				course = Course()
				savecourse(request,course)
				return redirect('editcourse', course_id=course.id)
			else:
				return render(request, 'topics/newcourse.html', {'topics': topics , 'error': 'Title and Topic fields are required'})	
	else:
		return render(request, 'topics/newcourse.html',{'topics': topics})
		
@login_required
def editcourse(request,course_id):
	course =  get_object_or_404(Course,pk=course_id) 
	topics = Topic.objects.all()
	print(course.id)

	if request.method == 'POST':
		if 'addglossary' in request.POST:
			return redirect('glossary', course_id=course.id)
		if 'newsection' in request.POST:
			numberofsections = course.section_set.count()
			section = Section()
			section.name = request.POST['sectionname']
			section.course = course
			section.order = numberofsections +1
			section.save()
			return redirect('editsection', section_id=section.id)
		if 'removelabel' in request.POST:
			label = request.POST['labelremove']
			course.label.remove(label)
			return redirect('editcourse', course_id=course.id)

		if 'newtopic' in request.POST:
			topic , created = Topic.objects.get_or_create(title=request.POST['topictitle'])
			topic.save()
			savecourse(request,course)
			course.topic  = topic
			course.save()
			return redirect('editcourse', course_id=course.id)

		if 'save' in request.POST:
			if request.POST['title'] and request.POST.getlist('topic'):
				savecourse(request,course)
				return redirect('editcourse', course_id=course.id)
			else:
				return render(request, 'topics/editcourse.html', {'topics': topics , 'course': course, 'error': 'Title and Topic fields are required'})
		
		if 'publish' in request.POST:
			if request.POST['title'] and request.POST.getlist('topic'):
				savecourse(request,course)
				course.published = True
				course.save()
				return redirect('teacher')
			else:
				return render(request, 'topics/editcourse.html', {'topics': topics , 'course': course, 'error': 'Title and Topic fields are required'})

	else:
		return render(request, 'topics/editcourse.html',{'topics': topics ,'course': course},)

def savecourse(request,course):

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

@login_required
def newsection(request, course_id):
	course =  get_object_or_404(Course,pk=course_id)
	numberofsections = course.section_set.count()
	
	if request.method == 'POST':
		if 'save' in request.POST:
			if request.POST['sectionname']:
				section = Section()
				section.name = request.POST['sectionname']
				section.course = course
				section.order = numberofsections +1
				section.save()
				return redirect('editsection', section_id=section.id)
			else:
				return render(request, 'topics/newsection.html',{'course': course,'error': 'Section name is required'})
	else:
		return render(request, 'topics/newsection.html',{'course': course})

		
@login_required
def editsection(request,section_id):
	section =  get_object_or_404(Section,pk=section_id)
	if request.method == 'POST':
		if 'save' in request.POST:
			if request.POST['sectionname']:
				section.name = request.POST['sectionname']
				section.save()
				return redirect('editsection', section_id=section.id)
			else:
				return render(request, 'topics/editsection.html', {'section': section, 'error': 'Name filed is required'})		
		elif 'submit_section' in request.POST:
			if request.POST['sectionname']:
				section.name = request.POST['sectionname']
				section.save()
				return redirect('editcourse', course_id=section.course.id)
			else:
				return render(request, 'topics/editsection.html', {'section': section, 'error': 'Name filed is required'})
		elif 'addresource' in request.POST:
			resource = Resource()
			resource.name = request.POST['resourcename']
			resource.link = request.FILES['resource']
			resource.section = section
			resource.save()
			return redirect('editsection', section_id=section.id)
		print("OSMANOSMAN")
		return redirect('home')
	else:
		return render(request, 'topics/editsection.html',{'section': section})

@login_required
def glossary(request, course_id):
	course =  get_object_or_404(Course,pk=course_id)
	return render(request, 'topics/glossary.html',{'course': course})


