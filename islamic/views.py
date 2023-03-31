from django.shortcuts import render
from quran import Quran
from django.core import serializers
from .models import *
from django.views.generic import TemplateView,FormView
from django.db.models import Q
from bs4 import BeautifulSoup
import requests

class HomeView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # quran = Quran()
        # quraan={1: 7, 2: 286, 3: 200, 4: 176, 5: 120, 6: 165, 7: 206, 8: 75, 9: 129, 10: 109, 11: 123, 12: 111, 13: 43, 14: 52, 15: 99, 16: 128, 17: 111, 18: 110, 19: 98, 20: 135, 21: 112, 22: 78, 23: 118, 24: 64, 25: 77, 26: 227, 27: 93, 28: 88, 29: 69, 30: 60, 31: 34, 32: 30, 33: 73, 34: 54, 35: 45, 36: 83, 37: 182, 38: 88, 39: 75, 40: 85, 41: 54, 42: 53, 43: 89, 44: 59, 45: 37, 46: 35, 47: 38, 48: 29, 49: 18, 50: 45, 51: 60, 52: 49, 53: 62, 54: 55, 55: 78, 56: 96, 57: 29, 58: 22, 59: 24, 60: 13, 61: 14, 62: 11, 63: 11, 64: 18, 65: 12, 66: 12, 67: 30, 68: 52, 69: 52, 70: 44, 71: 28, 72: 28, 73: 20, 74: 56, 75: 40, 76: 31, 77: 50, 78: 40, 79: 46, 80: 42, 81: 29, 82: 19, 83: 36, 84: 25, 85: 22, 86: 17, 87: 19, 88: 26, 89: 30, 90: 20, 91: 15, 92: 21, 93: 11, 94: 8, 95: 8, 96: 19, 97: 5, 98: 8, 99: 8, 100: 11, 101: 11, 102: 8, 103: 3, 104: 9, 105: 5, 106: 4, 107: 7, 108: 3, 109: 6, 110: 3, 111: 5, 112: 4, 113: 5, 114: 6}
        # s = list(quraan.keys())
        # a = list(quraan.values())
        
        # for i in s[23:]:
        #     surah = Surah.objects.get(number=i)
        #     for j in range(1,a[i-1]+1):
        #         ayah = quran.get_verse(i,j)['verse']
        #         juz = Juz.objects.get(number = ayah['juz_number'] )
        #         hizb = Hizb.objects.get(number = ayah['hizb_number'])
        #         num = ayah['verse_number']
        #         text = ayah['text_madani']
        #         Ayah.objects.create(surah=surah,juz=juz,hizb=hizb,number=num,text=text)
        #     print(f'Done [{i}]')
        ayah = Ayah.objects.all()
        surah = Surah.objects.all()
        context['ayahs'] = serializers.serialize('json', ayah)
        context['surahs'] = serializers.serialize('json', surah)
        return context

class SearchView(TemplateView):
    template_name = "search.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        kwa = "+".join(kw.split())
        url = f"https://surahquran.com/quran-search/search.php?search_word={kwa}"
        response = requests.get(url)
        # Create a BeautifulSoup object
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all div elements with a class of "example-div"
        div_tags = soup.find_all('div',class_="content")
        ayahs = []
        for div in div_tags:
            txt =set(div.find_all('a'))
            for i in txt:
                link = i['href'].replace('https://surahquran.com/','').replace('.html','')
                if link.startswith('english-aya'):
                    data = link.split('-')
                    data.pop(0)
                    ayahs.append((int(data[1]),int(data[-1])))
                else:
                    continue
        filter_ayah = []
        for aya in ayahs:  
            s = Surah.objects.get(number=aya[1])
            filter_ayah.append(Ayah.objects.get(surah=s,number=aya[0]))
        # for d in div_tags:
        #     output.append(d.text)
        context["results"] = filter_ayah 
        return context
       