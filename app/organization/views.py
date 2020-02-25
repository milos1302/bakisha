from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Organization


class OrganizationDetailView(DetailView):
    model = Organization

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['organization'].created_by:
            context['created_by'] = context['organization'].created_by.username
        return context


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


class OrganizationUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Organization
    template_name = 'organization/organization_update.html'
    fields = ['name', 'type']

    def test_func(self):
        is_administrator = self.request.user.groups.filter(name='Administrators').exists()
        is_org_owner = self.get_object().created_by.id == self.request.user.id
        return is_administrator and is_org_owner
