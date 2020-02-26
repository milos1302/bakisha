from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.contrib import messages
from .models import Game
from .forms import GameCreateForm


class GameListView(ListView):
    model = Game
    extra_context = {'title': 'Games'}


class GameDetailView(DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = self.object.players.all()
        context['title'] = self.object.name
        return context


class GameCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Game
    template_name = 'game/game_create.html'
    form_class = GameCreateForm
    extra_context = {'title': 'Create Game'}

    def test_func(self):
        return self.request.user.administrating_organizations.first() is not None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('game-update', kwargs={'slug': self.object.slug})


class GameUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Game
    template_name = 'game/game_update.html'
    fields = ['name', 'players', 'image']

    def test_func(self):
        return self.get_object().organization.administrators.filter(pk=self.request.user.pk).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update {self.object.name}'
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['image'].required = False
        return form


class GameDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Game
    success_url = '/games'

    def test_func(self):
        return self.get_object().organization.administrators.filter(pk=self.request.user.pk).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete {self.object.name}'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Game "{self.get_object().name}" has been successfully deleted.')
        return super().delete(request, *args, **kwargs)
