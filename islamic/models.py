from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Surah(models.Model):      
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    number_of_ayahs = models.IntegerField()
    revelation_type = models.CharField(max_length=100)
    maeni_asamuha = models.TextField(blank=True,null=True)
    sabab_tasmiatiha = models.TextField(blank=True,null=True)
    asmawuha = models.TextField(blank=True,null=True)
    maqsiduha_aleamu = models.TextField(blank=True,null=True)
    sabab_nuzuliha = models.TextField(blank=True,null=True)
    fadluha = models.TextField(blank=True,null=True)
    munasabatiha = models.TextField(blank=True,null=True)
    def __str__(self):
        return self.name
    
class Ayah(models.Model):
    surah = models.ForeignKey(Surah, on_delete=models.CASCADE)
    juz = models.ForeignKey('Juz', on_delete=models.CASCADE, related_name='ayahs')
    hizb = models.ForeignKey('Hizb', on_delete=models.CASCADE, related_name='ayahs')
    number = models.IntegerField()
    ar_number = models.CharField(max_length=4,blank=True,null=True)
    ayah_number_in_quraan = models.IntegerField(unique=True,blank=True,null=True)
    text = models.TextField()
    def __str__(self):
        return f"{self.surah.number}:{self.number}"

class Juz(models.Model):
    number = models.IntegerField()
    ar_number = models.CharField(max_length=3,blank=True,null=True)
   
    def __str__(self):
        return f"Juz {self.number}"
    
class Hizb(models.Model):
    number = models.IntegerField()
    ar_number = models.CharField(max_length=3,blank=True,null=True)

    def __str__(self):
        return f"Hizb {self.number}"

class Hadeeth(models.Model):
    hadeeth = models.TextField()
    class Meta:
        verbose_name_plural = 'Hadeeth'
    
    def __str__(self):
        return self.hadeeth
    
class Stories(models.Model):
    title = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = 'Stories'
    def __str__(self):
        return self.title

class StoryContent(models.Model):
    story = models.ForeignKey(Stories, on_delete=models.CASCADE)
    video_title = models.CharField(max_length=300) 
    video_url = models.URLField() 
    video_poster = models.URLField() 
    class Meta:
        verbose_name_plural = 'Story Content' 
    def __str__(self):
        return f"video for {self.story.title}"

class AzkarType(models.Model):
    zikr = models.CharField(max_length=250)
    
    class Meta:
        verbose_name_plural = 'Azkar Type'
    
    def __str__(self):
        return self.zikr

class AzkarContent(models.Model):
    zikr = models.ForeignKey(AzkarType, on_delete=models.CASCADE)
    content = models.TextField()
    repeat = models.IntegerField()
    
    class Meta:
        verbose_name_plural = 'Azkar Content'
    
    def __str__(self):
        return self.content

class DuaaType(models.Model):
    title = models.CharField(max_length=250)
    
    class Meta:
        verbose_name_plural = 'Duaa Type'
    
    def __str__(self):
        return self.title

class DuaaContent(models.Model):
    duaa = models.ForeignKey(DuaaType, on_delete=models.CASCADE)
    content = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Duaa Content'
    
    def __str__(self):
        return self.content

class RoqiahShareahType(models.Model):
    title = models.CharField(max_length=250)
    
    class Meta:
        verbose_name_plural = 'Roqiah Shareah Type'
    
    def __str__(self):
        return self.title

class RoqiahShareahContent(models.Model):
    roqiah = models.ForeignKey(RoqiahShareahType, on_delete=models.CASCADE)
    content = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Roqiah Shareah Content'
    
    def __str__(self):
        return self.content

class Sebha(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(33)],default=0)
    class Meta:
        verbose_name_plural = 'Sebha'
    def __str__(self):
        return self.name

class PrayLearningVideos(models.Model):
    video_title = models.CharField(max_length=300) 
    video_url = models.URLField() 
    video_poster = models.URLField() 
    class Meta:
        verbose_name_plural = 'Pray Learning Content' 
        
    def __str__(self):
        return self.video_title

class ArkanTypes(models.Model):
    title = models.CharField(max_length=250)
    
    class Meta:
        verbose_name_plural = 'Arkan Type'
    
    def __str__(self):
        return self.title
    
class ArkanContent(models.Model):
    rokn = models.ForeignKey(ArkanTypes, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Arkan Content'
    
    def __str__(self):
        return self.content

class IslamicAdvices(models.Model):
    advice = models.TextField()
    class Meta:
        verbose_name_plural = 'Islamic Advices'
    
    def __str__(self):
        return self.advice

class AsmaaAllahElhousnaa(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    class Meta:
        verbose_name_plural = 'Asmaa Allah Elhousnaa'
    def __str__(self):
        return self.name

class TajweedContent(models.Model):
    video_title = models.CharField(max_length=300) 
    video_url = models.URLField() 
    video_poster = models.URLField() 
    class Meta:
        verbose_name_plural = 'Tajweed Content' 
    def __str__(self):
        return self.video_title

class QuestionsAndAnswers(models.Model):
    question = models.TextField()
    Answer   = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Questions And Answers'
    
    def __str__(self):
        return self.question

class ChatHistory(models.Model):
    question = models.CharField(max_length=500)
    Answer   = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Chat History'
    
    def __str__(self):
        return self.question
