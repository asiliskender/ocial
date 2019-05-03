from django.urls import path, include
from . import views


urlpatterns = [
    path('',views.classroom, name= 'classroom'),
    path('teacher',views.teacher, name= 'teacher'),
	path('newcourse',views.newcourse, name= 'newcourse'),
	path('editcourse/<int:course_id>/', views.editcourse, name = 'editcourse'),
	path('course/<int:course_id>/glossary/', views.glossary, name = 'glossary'),
	path('editsection/<int:section_id>/', views.editsection, name = 'editsection'),
	path('editlecture/<int:lecture_id>/', views.editlecture, name = 'editlecture'),
	path('editquiz/<int:quiz_id>/', views.editquiz, name = 'editquiz'),
    path('editquestion/<int:question_id>/', views.editquestion, name = 'editquestion'),
	path('deletecourse/<int:course_id>/', views.deletecourse, name = 'deletecourse'),
    path('deletelabel/<int:course_id>/<int:label_id>/', views.deletelabel, name = 'deletelabel'),
    path('deletesection/<int:section_id>/', views.deletesection, name = 'deletesection'),
    path('deleteresource/<int:resource_id>/', views.deleteresource, name = 'deleteresource'),
    path('deletelecture/<int:lecture_id>/', views.deletelecture, name = 'deletelecture'),
    path('deletequiz/<int:quiz_id>/', views.deletequiz, name = 'deletequiz'),
    path('deletequestion/<int:question_id>/', views.deletequestion, name = 'deletequestion'),
    path('deletechoice/<int:choice_id>/', views.deletechoice, name = 'deletechoice'),


]
