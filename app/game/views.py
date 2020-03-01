from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from common.enums import CrudOperations
from common.utils.messages import Messenger
from common.utils.user_passes_test import UserPassesTest
from .models import Game
from .forms import GameCreateForm, GameUpdateForm

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
        return UserPassesTest.user_passes_test_with_message(self.request, CrudOperations.CREATE, Game)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        Messenger.crud_success(self.request, CrudOperations.CREATE, form.instance)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('game-detail', kwargs={'slug': self.object.slug})


class GameUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Game
    template_name = 'game/game_update.html'
    form_class = GameUpdateForm

    def test_func(self):
        return UserPassesTest.user_passes_test_with_message(self.request, CrudOperations.UPDATE, Game, self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update {self.object.name}'
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['image'].required = False
        return form

    def form_valid(self, form):
        Messenger.crud_success(self.request, CrudOperations.UPDATE, form.instance)
        return super().form_valid(form)


class GameDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Game
    success_url = '/games'

    def test_func(self):
        return UserPassesTest.user_passes_test_with_message(self.request, CrudOperations.DELETE, Game, self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete {self.object.name}'
        return context

    def delete(self, request, *args, **kwargs):
        Messenger.crud_success(self.request, CrudOperations.DELETE, self.get_object())
        return super().delete(request, *args, **kwargs)
