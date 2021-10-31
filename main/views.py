import os

from django.shortcuts import render
from django.views.generic import TemplateView


def index(request):
    """This is basic view for render your index."""
    return render(request, "index.html", {})


class MarkDown(TemplateView):
    """Rendering README.md on main page."""
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        markdowntext = open(
            os.path.join(os.path.abspath(os.path.dirname(__name__)), "README.md")
        ).read()

        context = super().get_context_data(**kwargs)
        context["markdowntext"] = markdowntext

        return context
