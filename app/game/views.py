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
    crud_operation = CrudOperations.CREATE

    def test_func(self):
        return UserPassesTest.user_passes_test_with_message(self.request, self.crud_operation, self.model)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.save()
        Messenger.crud_message(self.request, self.crud_operation, self.model)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('game-detail', kwargs={'slug': self.object.slug})


class GameUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Game
    template_name = 'game/game_update.html'
    form_class = GameUpdateForm
    crud_operation = CrudOperations.UPDATE

    def test_func(self):
        return UserPassesTest.user_passes_test_with_message(self.request, self.crud_operation,
                                                            self.model, self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update {self.object.name}'
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['image'].required = False
        return form

    def form_valid(self, form):
        Messenger.crud_message(self.request, self.crud_operation, self.model)
        return super().form_valid(form)


class GameDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Game
    success_url = '/games'
    crud_operation = CrudOperations.DELETE

    def test_func(self):
        return UserPassesTest.user_passes_test_with_message(self.request, self.crud_operation,
                                                            self.model, self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete {self.object.name}'
        return context

    def delete(self, request, *args, **kwargs):
        Messenger.crud_message(self.request, self.crud_operation, self.model)
        return super().delete(request, *args, **kwargs)
