import os

from django.shortcuts import render
from django.views.generic import TemplateView
from loguru import logger

from _settings.settings import BASE_DIR


def index(request):
    """This is basic view for render your index."""
    return render(request, "index.html", {})


class MarkDown(TemplateView):
    """Rendering README.MD on main page."""

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        path = os.path.join(BASE_DIR, "README.MD")
        logger.info(path)
        with open(path) as readme:
            markdowntext = readme.read()

        context = super().get_context_data(**kwargs)
        context["markdowntext"] = markdowntext

        return context
