from django.db import models

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