from django.contrib import admin
from .models import *

all_models = [Surah,Ayah,Juz,Hizb]
for mod in all_models:
    admin.site.register(mod)
