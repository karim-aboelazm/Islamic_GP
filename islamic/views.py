from django.shortcuts import render

from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'index.html'
    
class ProphetsStoriesView(TemplateView):
    template_name = "prophets_stories.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context[""] = 
        return context
    