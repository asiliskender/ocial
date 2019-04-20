from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from topics import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name= 'home'),
	path('accounts/', include('accounts.urls')),
    path('classroom/', include('topics.urls')),
    path('topics',views.topics, name= 'topics'),
    path('explore',views.explore, name= 'explore'),
    path('course/<int:course_id>/', views.coursedetail, name = 'coursedetail'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
