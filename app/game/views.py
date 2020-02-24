from django.views.generic import CreateView, ListView, DetailView
from .models import Game


class GameListView(ListView):
    model = Game


class GameDetailView(DetailView):
    model = Game


class GameCreateView(CreateView):
    model = Game
    fields = ['name', 'organization']
