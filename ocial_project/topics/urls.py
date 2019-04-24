from django.urls import path, include
from . import views


urlpatterns = [
    path('',views.classroom, name= 'classroom'),
    path('teacher',views.teacher, name= 'teacher'),
	path('newcourse',views.newcourse, name= 'newcourse'),
	path('editcourse/<int:course_id>/', views.editcourse, name = 'editcourse'),
	path('course/<int:course_id>/newsection/', views.newsection, name = 'newsection'),
	path('course/<int:course_id>/glossary/', views.glossary, name = 'glossary'),
	path('editsection/<int:section_id>/', views.editsection, name = 'editsection'),
]
