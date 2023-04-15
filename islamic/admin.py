from django.contrib import admin
from .models import *

all_models = [Surah,Ayah,Juz,Hizb,Hadeeth,Stories,StoryContent,
              DuaaType,DuaaContent,RoqiahShareahType,RoqiahShareahContent,Sebha,
              PrayLearningVideos,ArkanTypes,ArkanContent,IslamicAdvices,AsmaaAllahElhousnaa,
              AzkarType,AzkarContent,TajweedContent,QuestionsAndAnswers,ChatHistory]
for mod in all_models:
    admin.site.register(mod)

