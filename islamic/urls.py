from django.urls import path
from .views import *

app_name = 'islamic'

urlpatterns = [
    path(""                     , HomeView.as_view(),           name="home"       ),
    path("quraan-all-surahs/"   , QuraanListView.as_view(),     name="quraan_list"),
    path("stories/"             , StoriesView.as_view(),        name="stories"    ),
    path("search/"              , SearchView.as_view(),         name="search"     ),
    path("surah-<int:pk>/"      , QuraanPageView.as_view(),     name="quran"      ),
    path("ayah-<int:ayah_id>/"  , AyahSelectedInfo.as_view(),   name="ayah_info"  ),
    path("tafseer/"             , TafseerPageView.as_view(),    name="tafseer"    ),
    path("hadeeth/"             , HadeethView.as_view(),        name="hadeeth"    ),
    path("hisn-elmoslim/"       , HisnElmoslimView.as_view(),   name="hisn"       ),
    path("empty-chat/"          , EmptyChatView.as_view(),      name="echat"      ),
]