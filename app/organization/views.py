from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from common.enums import CrudOperations
from common.utils.user_passes_test import UserPassesTest
from common.utils.messages import Messenger
from .forms import OrganizationUpdateForm, OrganizationOwnerUpdateForm
from .models import Organization


class OrganizationListView(ListView):
    model = Organization
    extra_context = {'title': 'Organizations'}


class OrganizationDetailView(DetailView):
    model = Organization

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = self.object.members.all()
        context['title'] = self.object.name
        return context


class OrganizationCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Organization
    template_name = 'organization/organization_create.html'
    fields = ['name', 'type']
    extra_context = {'title': 'Create Organization'}

    def test_func(self):
        return UserPassesTest.user_passes_test_with_message(self.request, CrudOperations.CREATE, Organization)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.owner = self.request.user
        Messenger.crud_success(self.request, CrudOperations.CREATE, form.instance)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('organization-detail', kwargs={'slug': self.object.slug})


class OrganizationUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Organization
    template_name = 'organization/organization_update.html'

    def test_func(self):
        return UserPassesTest.user_passes_test_with_message(self.request, CrudOperations.UPDATE,
                                                            Organization, self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update {self.object.name}'
        return context

    def get_form_class(self):
        if self.request.user == self.get_object().owner:
            return OrganizationOwnerUpdateForm
        return OrganizationUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'owner': self.get_object().owner,
        })
        return kwargs

    def form_valid(self, form):
        Messenger.crud_success(self.request, CrudOperations.UPDATE, form.instance)
        return super().form_valid(form)


class OrganizationDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Organization
    success_url = '/organizations'

    def test_func(self):
        return UserPassesTest.user_passes_test_with_message(self.request, CrudOperations.DELETE,
                                                            Organization, self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete {self.object.name}'
        return context

    def delete(self, request, *args, **kwargs):
        Messenger.crud_success(self.request, CrudOperations.DELETE, self.get_object())
        return super().delete(request, *args, **kwargs)
