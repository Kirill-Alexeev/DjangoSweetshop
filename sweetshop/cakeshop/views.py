from django.shortcuts import render

from .models import Cake
from django.views import generic


def index(request):
    return render(
        request,
        "index.html",
        context={},
    )


class CakeListView(generic.ListView):
    model = Cake
    paginate_by = 12


class CakeDetailView(generic.DetailView):
    model = Cake
