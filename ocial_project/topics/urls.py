from django.urls import path, include
from . import views


urlpatterns = [
    path('',views.classroom, name= 'classroom'),
    path('teacher',views.teacher, name= 'teacher'),
	path('newcourse',views.newcourse, name= 'newcourse'),
	path('editcourse/<int:course_id>/', views.editcourse, name = 'editcourse'),

]
