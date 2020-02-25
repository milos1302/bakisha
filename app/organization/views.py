from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Organization


class OrganizationDetailView(DetailView):
    model = Organization

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = self.object.members.all()
        context['title'] = self.object.name
        return context


class OrganizationListView(ListView):
    model = Organization
    extra_context = {'title': 'Organizations'}


class OrganizationCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Organization
    template_name = 'organization/organization_create.html'
    fields = ['name', 'type']
    extra_context = {'title': 'Create Organization'}

    def test_func(self):
        return self.request.user.groups.filter(name='Administrators').exists()

    def form_valid(self, form):
        organization = form.save()
        organization.created_by = self.request.user
        organization.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('organization-update', kwargs={'slug': self.object.slug})


class OrganizationUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Organization
    fields = ['name', 'type', 'members']
    template_name = 'organization/organization_update.html'

    def test_func(self):
        is_administrator = self.request.user.groups.filter(name='Administrators').exists()
        is_org_admin = self.get_object().administrators.filter(id=self.request.user.id).exists()
        return is_administrator and is_org_admin

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update {self.object.name}'
        return context

    def form_valid(self, form):
        created_by = self.get_object().created_by
        if created_by and not form.cleaned_data.get('members').filter(pk=created_by.pk).exists():
            # User which created the organization should always be a member of that organization
            form.cleaned_data['members'] = form.cleaned_data.get('members').union(User.objects.filter(pk=created_by.pk))
        return super().form_valid(form)


class OrganizationDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Organization
    success_url = '/organizations'

    def test_func(self):
        return self.request.user == self.get_object().created_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete {self.object.name}'
        return context
