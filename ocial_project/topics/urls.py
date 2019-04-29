from django.urls import path, include
from . import views


urlpatterns = [
    path('',views.classroom, name= 'classroom'),
    path('teacher',views.teacher, name= 'teacher'),
	path('newcourse',views.newcourse, name= 'newcourse'),
	path('editcourse/<int:course_id>/', views.editcourse, name = 'editcourse'),
	path('course/<int:course_id>/glossary/', views.glossary, name = 'glossary'),
	path('editsection/<int:section_id>/', views.editsection, name = 'editsection'),
	path('deletecourse/<int:course_id>/', views.deletecourse, name = 'deletecourse'),
    path('deletelabel/<int:course_id>/<int:label_id>/', views.deletelabel, name = 'deletelabel'),
    path('deletesection/<int:course_id>/<int:section_id>/', views.deletesection, name = 'deletesection'),
    path('deleteresource/<int:section_id>/<int:resource_id>/', views.deleteresource, name = 'deleteresource'),
]
