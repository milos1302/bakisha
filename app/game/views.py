from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Game


class GameListView(ListView):
    model = Game


class GameDetailView(DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = self.object.players.all()
        return context


class GameCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Game
    fields = ['name', 'organization']

    def test_func(self):
        return self.request.user.groups.filter(name='Administrators').exists()
