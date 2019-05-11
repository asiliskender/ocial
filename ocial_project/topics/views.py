from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import *
from django.db.models import Count
import operator
import requests
import json
import hashlib
from itertools import chain
from django.core.files import File
from django.core.files.base import ContentFile





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

		if search_query != None:
			courses = Course.objects.filter(title__icontains=search_query, published=True)
		else:
			courses = Course.objects.filter(published=True)
			#courses = sorted(courses,reverse=True)
		return render(request, 'topics/explore.html', {'courses': courses})

def exploretopic(request,topic_id):
	topic =  get_object_or_404(Topic,pk=topic_id) 

	if request.method == 'GET': # If the form is submitted
		search_query = request.GET.get('search_course', None)

		if search_query != None:
			courses = Course.objects.filter(topic= topic_id,title__icontains=search_query, published=True)
		else:
			courses = Course.objects.filter(topic= topic_id,published=True)
			#courses = sorted(courses,reverse=True)
		return render(request, 'topics/explore.html', {'courses': courses,'topic': topic})

def exploreteacher(request,id):
	teacher =  get_object_or_404(User,pk=id) 

	if request.method == 'GET': # If the form is submitted
		search_query = request.GET.get('search_course', None)

		if search_query != None:
			courses = Course.objects.filter(teacher= id,title__icontains=search_query, published=True)
		else:
			courses = Course.objects.filter(teacher= id,published=True)
			#courses = sorted(courses,reverse=True)
		return render(request, 'topics/explore.html', {'courses': courses,'teacher': teacher})

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
		return render(request, 'topics/editcourse.html',{'topics': topics ,'course': course},)
	else:
		return render(request, 'topics/editcourse.html',{'topics': topics ,'course': course},)

def savecourse(request,course):
	if 'section-order' in request.POST:
		ordersection(request)

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
def glossary(request, course_id):
	course =  get_object_or_404(Course,pk=course_id)

	if 'search_glossary' in request.POST:
		API_ENDPOINT = "https://www.wikidata.org/w/api.php"
		query =  request.POST['search_glossary']
		params = {
		    'action': 'wbsearchentities',
		    'format': 'json',
		    'language': 'en',
		    'limit': '20',
		    'search': query
		}
		wiki_request = requests.get(API_ENDPOINT, params = params)
		r_json = wiki_request.json()['search']
		r_json = json.dumps(r_json)
		r_json = json.loads(r_json)
		return render(request, 'topics/glossary.html',{'course': course, 'r_json': r_json})
	else:
		return render(request, 'topics/glossary.html',{'course': course})

def newglossary(request,course_id,wiki_id):
	glossary = Glossary()
	course =  get_object_or_404(Course,pk=course_id)


	API_ENDPOINT = "https://www.wikidata.org/w/api.php"
	query =  wiki_id
	params = {
		    'action': 'wbsearchentities',
		    'format': 'json',
		    'language': 'en',
		    'limit': '1',
		    'search': query
		}
	wiki_request = requests.get(API_ENDPOINT, params = params)
	r_json = wiki_request.json()['search']
	r_json = json.dumps(r_json)
	r_json = json.loads(r_json)
	
	for entity in r_json:
		glossary.name = entity['label']
		glossary.description = entity['description']
		glossary.url = "https:" + entity['url']

	try:
		URL = "https://www.wikidata.org/w/api.php?action=wbgetclaims&entity={}&format=json".format(wiki_id)
		R = requests.get(URL).json()
		image_name= R['claims']['P18'][0]['mainsnak']['datavalue']['value']
		image_name = image_name.replace(' ', '_')
		md5sum = hashlib.md5(image_name.encode('utf-8')).hexdigest()
		a = md5sum[:1]
		ab = md5sum[:2]
		image_URL = "https://upload.wikimedia.org/wikipedia/commons/{}/{}/{}".format(a,ab,image_name)
		glossary.image_url = image_URL
	except:
		pass

	glossary.course = course
	glossary.save()
	return redirect('glossary', course_id=course.id)

@login_required
def deleteglossary(request,glossary_id):
	glossary =  get_object_or_404(Glossary,pk=glossary_id)
	course = glossary.course
	glossary.delete()
	return redirect('glossary', course_id=course.id)


@login_required
def deletecourse(request,course_id):
	course =  get_object_or_404(Course,pk=course_id)
	course.delete()
	return redirect('teacher')

@login_required
def deletelabel(request,label_id, course_id):
	label = get_object_or_404(Label,pk=label_id)
	course =  get_object_or_404(Course,pk=course_id)
	course.label.remove(label)
	return redirect('editcourse', course_id=course.id)



@login_required
def ordersection(request):
	if request.POST['section-order']:
		order_array = request.POST['section-order']
		order_array = order_array.split(',')

		i = 1
		for section_id in order_array:
			section = get_object_or_404(Section,pk=section_id)
			section.order = i
			section.save()
			i += 1

@login_required
def editsection(request,section_id):
	section =  get_object_or_404(Section,pk=section_id)
	learningpath = getlearningpath(section_id)

	if request.method == 'POST':
		if 'save_section' in request.POST:
			if request.POST['sectionname']:
				savesection(request,section)
				return redirect('editsection', section_id=section.id)
			else:
				return render(request, 'topics/editsection.html', {'section': section, 'error': 'Name field is required'})		
		if 'submit_section' in request.POST:
			if request.POST['sectionname']:
				savesection(request,section)
				return redirect('editcourse', course_id=section.course.id)
			else:
				return render(request, 'topics/editsection.html', {'section': section, 'error': 'Name field is required'})
		if 'addresource' in request.POST:
			if request.FILES.get('resource', False) and request.POST['resourcename']:
				resource = Resource()
				resource.name = request.POST['resourcename']
				resource.link = request.FILES['resource']
				resource.section = section
				resource.save()
				return redirect('editsection', section_id=section.id)
			else:
				return render(request, 'topics/editsection.html', {'section': section, 'learningpath': learningpath, 'error': 'Resource and Resource Name fields are required'})
		if 'newlecture' in request.POST:
			if request.POST['itemtitle']:
				lecture = Lecture()
				lecture.title = request.POST['itemtitle']
				lecture.section = section
				lecture.order = len(learningpath)+1
				lecture.save()
				return redirect('editlecture', lecture_id=lecture.id)
		if 'newquiz' in request.POST:
			if request.POST['itemtitle']:
				quiz = Quiz()
				quiz.title = request.POST['itemtitle']
				quiz.section = section
				quiz.order = len(learningpath)+1
				quiz.save()
				return redirect('editquiz', quiz_id=quiz.id)
		return render(request, 'topics/editsection.html',{'section': section, 'learningpath': learningpath})
	else:
		return render(request, 'topics/editsection.html',{'section': section, 'learningpath': learningpath})

def savesection(request,section):
	
	if 'lp-order' in request.POST:
		orderlp(request)

	section.name = request.POST['sectionname']
	section.description = request.POST['sectiondescription']
	section.save()

@login_required
def orderlp(request):
	if request.POST['lp-order']:
		order_array = request.POST['lp-order']
		order_array = order_array.split(',')

		i = 1
		for lp_item in order_array:
			item = lp_item.split(':')
			itemtype = item[0]
			itemid = item[1]
			if itemtype == Lecture._meta.verbose_name:
				lecture = get_object_or_404(Lecture,pk=itemid)
				lecture.order = i
				lecture.save()
			elif itemtype == Quiz._meta.verbose_name:
				quiz = get_object_or_404(Quiz,pk=itemid)
				quiz.order = i
				quiz.save()
			i += 1


def getlearningpath(section_id):
    lectures = Lecture.objects.filter(section= section_id)
    quizs = Quiz.objects.filter(section= section_id)
    learningpath = sorted(
        chain(lectures, quizs),
        key=lambda item: item.order, reverse=False)
    return learningpath

@login_required
def deletesection(request,section_id):
	section = get_object_or_404(Section,pk=section_id)
	course_id = section.course.id
	section.delete()
	return redirect('editcourse', course_id=course_id)


@login_required
def deleteresource(request,resource_id):
	resource = get_object_or_404(Resource,pk=resource_id)
	section_id = resource.section.id
	resource.delete()
	return redirect('editsection', section_id=section_id)


def editlecture(request, lecture_id):
	lecture =  get_object_or_404(Lecture,pk=lecture_id)
	if request.method == 'POST':
		if 'save_lecture' in request.POST:
			if request.POST['lecturetitle']:
				savelecture(request,lecture)
				return redirect('editlecture', lecture_id=lecture.id)
			else:
				return render(request, 'topics/editlecture.html', {'lecture': lecture, 'error': 'Title field is required'})		
		if 'submit_lecture' in request.POST:
			if request.POST['lecturetitle']:
				savelecture(request,lecture)
				return redirect('editsection', section_id=lecture.section.id)
			else:
				return render(request, 'topics/editlecture.html', {'lecture': lecture, 'error': 'Title field is required'})		
		return render(request, 'topics/editlecture.html',{'lecture': lecture})
	else:
		return render(request, 'topics/editlecture.html',{'lecture': lecture})

@login_required
def deletelecture(request,lecture_id):
	lecture = get_object_or_404(Lecture,pk=lecture_id)
	section_id = lecture.section.id
	lecture.delete()
	return redirect('editsection', section_id=section_id)

def savelecture(request,lecture):
	
	lecture.title = request.POST['lecturetitle']
	lecture.body = request.POST['lecturebody']
	lecture.save()

def editquiz(request, quiz_id):
	quiz =  get_object_or_404(Quiz,pk=quiz_id)
	if request.method == 'POST':
			if 'save_quiz' in request.POST:
				if request.POST['quiztitle']:
					savequiz(request,quiz)
					return redirect('editquiz', quiz_id=quiz.id)
				else:
					return render(request, 'topics/editquiz.html', {'quiz': quiz, 'error': 'Quiz title field is required'})		
			if 'submit_quiz' in request.POST:
				if request.POST['quiztitle']:
					savequiz(request,quiz)
					return redirect('editsection', section_id=quiz.section.id)
				else:
					return render(request, 'topics/editquiz.html', {'quiz': quiz, 'error': 'Quiz title field is required'})		
			if 'newquestion' in request.POST:
				if request.POST['questiontitle']:
					numberofquestions = quiz.question_set.count()
					question = Question()
					question.title = request.POST['questiontitle']
					question.quiz = quiz
					question.order = numberofquestions+1
					question.save()
					return redirect('editquestion', question_id=question.id)
			return render(request, 'topics/editquiz.html',{'quiz': quiz})
	else:
		return render(request, 'topics/editquiz.html',{'quiz': quiz})

def savequiz(request,quiz):
	
	orderquestion(request)

	quiz.title = request.POST['quiztitle']
	quiz.successrate = request.POST['quizsuccessrate']
	quiz.save()

@login_required
def orderquestion(request):
	if request.POST['question-order']:
		order_array = request.POST['question-order']
		order_array = order_array.split(',')
		print(order_array)

		i = 1
		for question_id in order_array:
			question = get_object_or_404(Question,pk=question_id)
			question.order = i
			question.save()
			i += 1

@login_required
def deletequiz(request,quiz_id):
	quiz = get_object_or_404(Quiz,pk=quiz_id)
	section_id = quiz.section.id
	quiz.delete()
	return redirect('editsection', section_id=section_id)

def editquestion(request, question_id):
	question =  get_object_or_404(Question,pk=question_id)
	if request.method == 'POST':
			if 'save_question' in request.POST:
				if request.POST['questiontitle']:
					savequestion(request,question)
					return redirect('editquestion', question_id=question.id)
				else:
					return render(request, 'topics/editquiz.html', {'quiz': quiz, 'error': 'Quiz title field is required'})		
			if 'submit_question' in request.POST:
				if request.POST['questiontitle']:
					savequestion(request,question)
					return redirect('editquiz', quiz_id=question.quiz.id)
				else:
					return render(request, 'topics/editquiz.html', {'quiz': quiz, 'error': 'Quiz title field is required'})		
			if 'newchoice' in request.POST:
				if request.POST['choicetitle']:
					numberofchoices = question.choice_set.count()
					choice = Choice()
					choice.title = request.POST['choicetitle']
					choice.question = question
					choice.order = numberofchoices + 1
					choice.save()
					return redirect('editquestion', question_id=question.id)
			elif 'choicetitleedit' in request.POST:
				if request.POST['edit_choicetitle']:
					choice_id = request.POST['edit_choiceid']
					choice = get_object_or_404(Choice,pk=choice_id)
					choice.title = request.POST['edit_choicetitle']
					choice.save()
				return redirect('editquestion', question_id=question.id)
			return render(request, 'topics/editquestion.html',{'question': question})
	else:
		return render(request, 'topics/editquestion.html',{'question': question})

@login_required
def deletequestion(request,question_id):
	question = get_object_or_404(Question,pk=question_id)
	quiz_id = question.quiz.id
	question.delete()
	return redirect('editquiz', quiz_id=quiz_id)

@login_required
def savequestion(request,question):
	
	orderchoice(request)

	question.title = request.POST['questiontitle']
	question.save()

@login_required
def orderchoice(request):
	if request.POST['choice-order']:
		order_array = request.POST['choice-order']
		order_array = order_array.split(',')

		print(request.POST)

		if 'choice-radio' in request.POST:
			trueChoice = request.POST['choice-radio']
		else:
			trueChoice = -1

		i = 1
		for choice_id in order_array:
			choice = get_object_or_404(Choice,pk=choice_id)
			choice.order = i
			if choice_id == trueChoice:
				choice.isTrue = True
			else:
				choice.isTrue = False
			choice.save()
			i += 1

@login_required
def deletechoice(request,choice_id):
	choice = get_object_or_404(Choice,pk=choice_id)
	question_id = choice.question.id
	choice.delete()
	return redirect('editquestion', question_id=question_id)
