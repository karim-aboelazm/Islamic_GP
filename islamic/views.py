# -*- coding: utf-8 -*-
from    django.views.generic        import TemplateView,DetailView,View
from    django.db.models.functions  import Length
from    django.shortcuts            import redirect
from    django.core                 import serializers
from    django.db.models            import Q,F
from    bs4                         import BeautifulSoup
from    .models                     import *
import  requests,salat,pytz,datetime as dt

'''
    get_tafsir(tafsir_type,surah_number,ayah_number) Function
    ----------------------------------------------------------
    * get Ayah Tafsir based on 
        1) surah_number
        2) ayah_number
        3) tafsir_type 
    getting From https://surahquran.com/
    Using Web scraping to get this information(BeautifulSoup)

'''
def get_tafsir(tt,ns,na):
    url         = f'https://tafsir.app/{tt}/{ns}/{na}'
    response    = requests.get(url)
    soup        = BeautifulSoup(response.content, "html.parser")
    divs        = soup.find_all("div", {"id": "preloaded-text"})
    text        = ""
    for div in divs:
        text += div.text
    return text

'''
    get_eraab(surah_number,ayah_number) Function
    --------------------------------------------
    * get Ayah E3raab based on 
        1) surah_number --> ns
        2) ayah_number  --> na
    getting From https://surahquran.com/
    Using Web scraping to get this information(BeautifulSoup)

'''
def get_eraab(ns,na):
    url         = f'https://surahquran.com/quran-search/e3rab-aya-{na}-sora-{ns}.html'
    response    = requests.get(url)
    soup        = BeautifulSoup(response.content, "html.parser")
    divs        = soup.find_all("div", {"class": "card-body"})
    ancor       = soup.find('a', href=f"https://surahquran.com/quran-expressed/{ns}.html")
    text        = ""
    for p in divs[1].find_all('p'):
        text += '' if "إعراب الصفحة" in p.text else p.text
    return text

'''
    get_ayah_mp3(surah_number,ayah_number) Function
    -----------------------------------------------
    * get ayah audio based on 
        1) surah_number --> ns
        2) ayah_number  --> na
    getting from https://surahquran.com/
    Using Web scraping to get this information(BeautifulSoup)
'''
def get_ayah_mp3(ns,na):
    url         = f'https://surahquran.com/aya-{na}-sora-{ns}.html'
    response    = requests.get(url)
    soup        = BeautifulSoup(response.content, "html.parser")
    divs        = soup.find("audio")
    return divs.source['src'].replace("MaherAlMuaiqly128kbps","Alafasy_128kbps")

'''
    get_prayer_times() Function
    -----------------------------
    * get all prayer times based on
        1) longitude
        2) latitude
        3) Time Zone 
    using salat Python Library
'''
def get_prayer_times():
    pt                        = salat.PrayerTimes(salat.CalculationMethod.EGYPT, salat.AsrMethod.STANDARD)
    now                       = dt.datetime.now()
    date                      = dt.date(now.year,now.month,now.day)
    latitude,longitude        = 30.044420,31.235712
    eastern                   = pytz.timezone('Africa/Cairo')
    prayer_times              = pt.calc_times(date, eastern, longitude, latitude)
    times                     = []
    for name, time in prayer_times.items():
        readable_time = time.strftime("%I:%M %p")  
        if name == "sunrise" or name == "midnight":
            continue
        else:
            if "AM" in readable_time:
                readable_time = readable_time.replace('AM',"ص")
            else:
                readable_time = readable_time.replace("PM","م")
            readable_time     = readable_time.translate(str.maketrans('0123456789','٠١٢٣٤٥٦٧٨٩'))
            times.append(readable_time)
    return times

'''
    Home Page (First Page) Backend (TemplateView)
    ------------------------------
    * It has :
        1) Asmaauallh Elhosnaa inside it 
        2) Prayer Times
        3) Quraan Ayaht sequence Display 
        4) chatbot for any Islamic Question 
        5) Random Duaa display every 10 seconds
'''
class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context                 = super().get_context_data(**kwargs)
        message                 = self.request.GET.get('ask') if self.request.GET.get('ask') else ""
        context['ayahs']        = serializers.serialize('json', Ayah.objects.all())
        context['surahs']       = serializers.serialize('json', Surah.objects.all())
        context['hizbs']        = serializers.serialize('json', Hizb.objects.all())
        context['juzs']         = serializers.serialize('json', Juz.objects.all())
        context['fajr']         = get_prayer_times()[0]
        context['dhur']         = get_prayer_times()[1]
        context['asr']          = get_prayer_times()[2]
        context['maghrib']      = get_prayer_times()[3]
        context['isha']         = get_prayer_times()[4]
        context["Allah_names"]  = [i.name for i in AsmaaAllahElhousnaa.objects.all()[1:]]
        context["duaas"]        = DuaaContent.objects.annotate(text_len=Length('content')).filter(text_len__lte=60).values_list(F('content'), flat=True)
        response                = QuestionsAndAnswers.objects.filter(Q(question__icontains=message))
        if response:
            ans                 = response.first().Answer
            question            = response.first().question
            if not ChatHistory.objects.filter(question=question).exists(): 
                chat            = ChatHistory.objects.create(question=question,Answer=ans)
            context['response'] = ans
            context["chat"]     = ChatHistory.objects.all()
        else:
            pass
        return context

'''
    Quraan List Page (Second Page) Backend (TemplateView) 
    ------------------------------
    * It has :
        1) The Whole Quraan Indexes Surah
        2) Tajweed Teaching Playlist
        3) search bar to search for any ayah based on any part on it 
        4) Tafsir bar (selection bar) to choose tafsir type and type ayah to get tafsir
        
'''    
class QuraanListView(TemplateView):
    template_name               = 'quraan_list.html'
    def get_context_data(self, **kwargs):
        context                 = super().get_context_data(**kwargs)
        context['all_surahs']   = Surah.objects.all()
        context["tajweed"]      = TajweedContent.objects.all()
        return context

'''
    Quraan Surah Page (Third Page) Backend (DetailView) concatinate with [Quraan List Page]
    ------------------------------
    * It has :
        1) The Surah Text for each surah based on surah id
        2) each ayah on surah is clickable to show its tafsir and audio 
''' 
class QuraanPageView(DetailView):
    template_name                ="quraan.html"
    model                        = Surah
    def get_context_data(self, **kwargs):
        context                  = super().get_context_data(**kwargs)
        context["current_surah"] = context['object']
        return context
  
'''
    Search Page (Forth Page) Backend (TemplateView) concatinate with [Quraan List Page]
    ------------------------------
    * It has :
        1) The Surah Text for each surah based on surah id
        2) each ayah on surah is clickable to show its tafsir and audio 
'''     
class SearchView(TemplateView):
    template_name            = "search.html"
    def get_context_data(self, **kwargs):
        context              = super().get_context_data(**kwargs)
        kw                   = self.request.GET.get("keyword")
        kwa                  = "+".join(kw.split())
        url                  = f"https://surahquran.com/quran-search/search.php?search_word={kwa}"
        response             = requests.get(url)
        soup                 = BeautifulSoup(response.content, 'html.parser')
        div_tags             = soup.find_all('div', class_="content")
        ayahs                = []
        page_count_element   = soup.find("ul", class_="pagination")
        if page_count_element is None:
            for div in div_tags:
                txt           = set(div.find_all('a'))
                for i in txt:
                    link      = i['href'].replace('https://surahquran.com/', '').replace('.html', '')
                    if link.startswith('english-aya'):
                        data  = link.split('-')
                        data.pop(0)
                        ayahs.append((int(data[1]), int(data[-1])))
                    else:
                        continue
        else:
            page_count         = len(page_count_element.find_all("li")) - 2 
            for page in range(1, page_count + 1):
                page_url       = f"{url}&page={page}"
                page_response  = requests.get(page_url)
                page_soup      = BeautifulSoup(page_response.content, 'html.parser')
                page_div_tags  = page_soup.find_all('div', class_="content")
                for div in page_div_tags:
                    txt        = set(div.find_all('a'))
                    for i in txt:
                        link   = i['href'].replace('https://surahquran.com/', '').replace('.html', '')
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
        context["results"] = filter_ayah 
        return context  

'''
    Tafsir Page (Fifth Page) Backend (TemplateView) concatinate with [Quraan List Page]
    ------------------------------
    * It has :
        1) Ayah tafsir display based on tafsir type and ayah text
''' 
class TafseerPageView(TemplateView):
    template_name           = "tafseer.html"
    def get_context_data(self, **kwargs):
        context             = super().get_context_data(**kwargs)
        kw                  = self.request.GET.get("t_ayah")
        tkw                 = self.request.GET.get("tafseer")
        tafseer_type        = ''
        tafseer_ar_type     = ''
        if tkw == '1':
            tafseer_type    = 'saadi'
            tafseer_ar_type = 'السعدي'
        elif tkw == '2':
            tafseer_type    = 'baghawi'
            tafseer_ar_type = 'البغوي'
        elif tkw == '3':
            tafseer_type    = 'ibn-katheer'
            tafseer_ar_type = 'ابن كثير'
        elif tkw == '4':
            tafseer_type    = 'qurtubi'
            tafseer_ar_type = 'القرطبي'
        elif tkw == '5':
            tafseer_type    = 'tabari'
            tafseer_ar_type = 'الطبري'
        else:
            pass
        kwa                 = "+".join(kw.split())
        url                 = f"https://surahquran.com/quran-search/search.php?search_word={kwa}"
        response            = requests.get(url)
        soup                = BeautifulSoup(response.content, 'html.parser')
        div_tags            = soup.find_all('div',class_="content")
        ayahs               = []
        for div in div_tags:
            txt             = set(div.find_all('a'))
            for i in txt:
                link        = i['href'].replace('https://surahquran.com/','').replace('.html','')
                if link.startswith('english-aya'):
                    data    = link.split('-')
                    data.pop(0)
                    ayahs.append((int(data[1]),int(data[-1])))
                else:
                    continue
        filter_ayah         = []
        for aya in ayahs:  
            filter_ayah.append(aya)
        context["tafseer_result"] = get_tafsir(tafseer_type,filter_ayah[0][1],filter_ayah[0][0]) if len(filter_ayah) > 0 else ''
        context["ayah"]           = Ayah.objects.get(surah=filter_ayah[0][1],number=filter_ayah[0][0]) if len(filter_ayah) > 0 else ''
        context["tafseer_ar"]     = tafseer_ar_type
        return context 

'''
    Ayah Info Page (sixth Page) Backend (TemplateView) concatinate with [Quraan Surah Page]
    ------------------------------
    * It has :
        1) Ayah with all tafsirs and audio to know it's correct pronunciation
'''
class AyahSelectedInfo(TemplateView):
    template_name = "aya_info.html"
    def get_context_data(self, **kwargs):
        context                 = super().get_context_data(**kwargs)
        ayah                    = Ayah.objects.get(id=kwargs['ayah_id'])
        context['tafseer_ar1']  = 'السعدي'
        context['tafseer_ar2']  = 'البغوي'
        context['tafseer_ar3']  = 'ابن كثير'
        context['tafseer_ar4']  = 'القرطبي'
        context['tafseer_ar5']  = 'الطبري'
        context["ayah"]         = ayah
        context['eraab']        = get_eraab(int(ayah.surah.number),int(ayah.number))
        context['tafseer1']     = get_tafsir('saadi',ayah.surah.number,ayah.number)
        context['tafseer2']     = get_tafsir('baghawi',ayah.surah.number,ayah.number)
        context['tafseer3']     = get_tafsir('ibn-katheer',ayah.surah.number,ayah.number)
        context['tafseer4']     = get_tafsir('qurtubi',ayah.surah.number,ayah.number)
        context['tafseer5']     = get_tafsir('tabari',ayah.surah.number,ayah.number)
        context['aya_mp3']      = get_ayah_mp3(ayah.surah.number,ayah.number)
        return context
 
'''
    Stories Page (Seventh Page) Backend (TemplateView) 
    ------------------------------
    * It has :
        1) Playlists for prophit , Humans , Animals and Quraan Stories 
'''  
class StoriesView(TemplateView):
    template_name = "stories.html"
    def get_context_data(self, **kwargs):
        context                = super().get_context_data(**kwargs)
        tkw                    = self.request.GET.get("story")
        if tkw == '1':
            story_name         = 'قصص الانبياء'
            story_num          = Stories.objects.get(title="الانبياء")
        elif tkw == '2':
            story_name         = 'قصص الانسان'
            story_num          = Stories.objects.get(title="الانسان")
        elif tkw == '3':
            story_name         = 'قصص الحيوانات'
            story_num          = Stories.objects.get(title="الحيوانات")
        elif tkw == '4':
            story_name         = 'قصص عجائب القرأن'
            story_num          = Stories.objects.get(title="عجائب القرأن")
        else:
            story_num          = Stories.objects.get(title="الانبياء")
        context["story"]       = story_num 
        context["all_stories"] = Stories.objects.all()
        return context

'''
    Ahadith Page (Eight Page) Backend (TemplateView) 
    ------------------------------
    * It has :
        1) 500 hadith 
'''  
class HadeethView(TemplateView):
    template_name               = "hadeeth.html"
    def get_context_data(self, **kwargs):
        context                 = super().get_context_data(**kwargs)
        context["hadeeth_list"] = Hadeeth.objects.all() 
        return context
  
'''
    Hisn Elmoslem Page (Ninth Page) Backend (TemplateView) 
    ------------------------------
    * It has :
        1) All Types of Azkar 
        2) All Types of Duaa
        3) All Types of Rouqia 
        4) All Types of Tasbeeh
''' 
class HisnElmoslimView(TemplateView):
    template_name             = "hisn_elmoslim.html" 
    def get_context_data(self, **kwargs):
        context               = super().get_context_data(**kwargs)
        context["zikr_list"]  = AzkarType.objects.all()
        context["duaa_list"]  = DuaaType.objects.all()
        context["roqia_list"] = RoqiahShareahType.objects.all()
        context["arkan_list"] = ArkanTypes.objects.all()
        context["sebha_list"] = Sebha.objects.all()
        return context

'''
    Empty Chat Class (Ninth Page) Backend (View) 
    ------------------------------
    remove History data in chatbot
''' 
class EmptyChatView(View):
    def get(self, request, *args, **kwargs):
        action    = request.GET.get('action')
        if action == 'del':
            ChatHistory.objects.all().delete()
        else:
            pass
        return redirect('/')