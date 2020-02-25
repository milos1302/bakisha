from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .models import Organization


class OrganizationDetailView(DetailView):
    model = Organization


class OrganizationListView(ListView):
    model = Organization

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrganizationCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Organization
    template_name = 'organization/organization_create.html'
    fields = ['name', 'type']

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
    template_name = 'organization/organization_update.html'
    fields = ['name', 'type', 'members']

    def test_func(self):
        is_administrator = self.request.user.groups.filter(name='Administrators').exists()
        is_org_admin = self.get_object().administrators.filter(id=self.request.user.id).exists()
        # is_org_owner = self.get_object().created_by.id == self.request.user.id
        return is_administrator and is_org_admin
