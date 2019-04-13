from django.urls import path, include
from . import views


urlpatterns = [
    path('newcourse',views.newcourse, name= 'newcourse'),
]
