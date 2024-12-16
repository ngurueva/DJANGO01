from typing import Any
from django.http import HttpResponse
from django.shortcuts import render
from museum.models import Exhibit
from django.views import View
from django.views.generic import TemplateView

# Create your views here.



class ShowExhibitsView(TemplateView):
    template_name = "exhibits/show_exhibits.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['exhibits'] = Exhibit.objects.all()

        return context
