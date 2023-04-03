from django.shortcuts import render
from quran import Quran
from django.core import serializers
from .models import *
from django.views.generic import TemplateView,FormView,DetailView
from django.db.models import Q
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404
import requests
import json


    
def get_tafsir(tt,ns,na):
    url = f'https://tafsir.app/{tt}/{ns}/{na}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    divs = soup.find_all("div", {"id": "preloaded-text"})
    text = ""
    for div in divs:
        text += div.text
    return text

def get_eraab(ns,na):
    url = f'https://surahquran.com/quran-search/e3rab-aya-{na}-sora-{ns}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    divs = soup.find_all("div", {"class": "card-body"})
    ancor = soup.find('a', href=f"https://surahquran.com/quran-expressed/{ns}.html")
    text = ""
    for p in divs[1].find_all('p'):
        text += '' if "إعراب الصفحة" in p.text else p.text
    return text

def get_ayah_mp3(ns,na):
    url = f'https://surahquran.com/aya-{na}-sora-{ns}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    divs = soup.find("audio")
    return divs.source['src'].replace("MaherAlMuaiqly128kbps","Alafasy_128kbps")

class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ayahs'] = serializers.serialize('json', Ayah.objects.all())
        context['surahs'] = serializers.serialize('json', Surah.objects.all())
        context['hizbs'] = serializers.serialize('json', Hizb.objects.all())
        context['juzs'] = serializers.serialize('json', Juz.objects.all())
        return context
    
class QuraanListView(TemplateView):
    template_name = 'quraan_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_surahs'] = Surah.objects.all()   
        return context

class QuraanPageView(DetailView):
    template_name="quraan.html"
    model = Surah
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_surah"] = context['object']
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

        # Extract all div elements with a class of "content"
        div_tags = soup.find_all('div', class_="content")
        ayahs = []

        # Find the total number of pagination pages
        page_count_element = soup.find("ul", class_="pagination")
        if page_count_element is None:
            # There is only one page, so just scrape the data from the first page
            for div in div_tags:
                txt = set(div.find_all('a'))
                for i in txt:
                    link = i['href'].replace('https://surahquran.com/', '').replace('.html', '')
                    if link.startswith('english-aya'):
                        data = link.split('-')
                        data.pop(0)
                        ayahs.append((int(data[1]), int(data[-1])))
                    else:
                        continue
        else:
            # There are multiple pages, so scrape the data from each page
            page_count = len(page_count_element.find_all("li")) - 2  # subtract 2 for the "Previous" and "Next" buttons
            for page in range(1, page_count + 1):
                page_url = f"{url}&page={page}"
                page_response = requests.get(page_url)
                page_soup = BeautifulSoup(page_response.content, 'html.parser')
                page_div_tags = page_soup.find_all('div', class_="content")
                for div in page_div_tags:
                    txt = set(div.find_all('a'))
                    for i in txt:
                        link = i['href'].replace('https://surahquran.com/', '').replace('.html', '')
                        if link.startswith('english-aya'):
                            data = link.split('-')
                            data.pop(0)
                            ayahs.append((int(data[1]), int(data[-1])))
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

class TafseerPageView(TemplateView):
    template_name = "tafseer.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("t_ayah")
        tkw = self.request.GET.get("tafseer")
        tafseer_type = ''
        tafseer_ar_type = ''
        if tkw == '1':
            tafseer_type = 'saadi'
            tafseer_ar_type = 'السعدي'
        elif tkw == '2':
            tafseer_type = 'baghawi'
            tafseer_ar_type = 'البغوي'
        elif tkw == '3':
            tafseer_type = 'ibn-katheer'
            tafseer_ar_type = 'ابن كثير'
        elif tkw == '4':
            tafseer_type = 'qurtubi'
            tafseer_ar_type = 'القرطبي'
        elif tkw == '5':
            tafseer_type = 'tabari'
            tafseer_ar_type = 'الطبري'
        else:
            pass
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
            filter_ayah.append(aya)
            # filter_ayah.append(Ayah.objects.get(surah=s,number=aya[0]))
        context["tafseer_result"]= get_tafsir(tafseer_type,filter_ayah[0][1],filter_ayah[0][0]) if len(filter_ayah) > 0 else ''
        context["ayah"] = Ayah.objects.get(surah=filter_ayah[0][1],number=filter_ayah[0][0]) if len(filter_ayah) > 0 else ''
        context["tafseer_ar"] = tafseer_ar_type
        return context 

class AyahSelectedInfo(TemplateView):
    template_name = "aya_info.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Define a function to convert Arabic numbers to English
        ayah = Ayah.objects.get(id=kwargs['ayah_id'])
        context["ayah"] = ayah
        context['eraab'] = get_eraab(int(ayah.surah.number),int(ayah.number))
        tafseer1 = 'saadi'
        tafseer2 = 'baghawi'
        tafseer3 = 'ibn-katheer'
        tafseer4 = 'qurtubi'
        tafseer5 = 'tabari'
        context['tafseer_ar1'] = 'السعدي'
        context['tafseer_ar2'] = 'البغوي'
        context['tafseer_ar3'] = 'ابن كثير'
        context['tafseer_ar4'] = 'القرطبي'
        context['tafseer_ar5'] = 'الطبري'
        context['tafseer1'] = get_tafsir(tafseer1,ayah.surah.number,ayah.number)
        context['tafseer2'] = get_tafsir(tafseer2,ayah.surah.number,ayah.number)
        context['tafseer3'] = get_tafsir(tafseer3,ayah.surah.number,ayah.number)
        context['tafseer4'] = get_tafsir(tafseer4,ayah.surah.number,ayah.number)
        context['tafseer5'] = get_tafsir(tafseer5,ayah.surah.number,ayah.number)
        context['aya_mp3'] = get_ayah_mp3(ayah.surah.number,ayah.number)
        return context
    
class ProphetsStoriesView(TemplateView):
    template_name = "prophets_stories.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context[""] = 
        return context
