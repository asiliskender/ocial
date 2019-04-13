from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Topic, Course

def home(request):
	topics = Topic.objects.all()
	return render(request, 'topics/home.html', {'topics': topics})


@login_required
def newcourse(request):
	topics = Topic.objects.all()
	if request.method == 'POST':
		if request.POST['title'] and request.POST.getlist('topic'):
			course = Course()
			course.title = request.POST['title']
			course.description = request.POST['description']
			course.pubdate = timezone.datetime.now()
			course.teacher = request.user

			topic_title = request.POST.get('topic')
			course.topic  = Topic.objects.get(id=topic_title)

		

			if request.FILES.get('image', False):
				course.image = request.FILES['image']

			course.save()
			return redirect('home')
		else:
			return render(request, 'topics/newcourse.html', {'topics': topics , 'error': 'Title and Topic fields are required'})	
	else:
		return render(request, 'topics/newcourse.html',{'topics': topics})