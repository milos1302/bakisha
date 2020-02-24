from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Game
from .forms import GameCreateForm


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
    form_class = GameCreateForm

    def test_func(self):
        return self.request.user.groups.filter(name='Administrators').exists()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
