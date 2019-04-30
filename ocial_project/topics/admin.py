from django.contrib import admin
from .models import *


admin.site.register(Topic)
admin.site.register(Course)
admin.site.register(Label)
admin.site.register(Glossary)
admin.site.register(Section)
admin.site.register(Lecture)
admin.site.register(Quiz)
admin.site.register(Resource)