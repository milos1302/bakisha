from django.views.generic import DetailView, ListView, CreateView
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
        print(context['organization_list'][1].created_by)
        return context


class OrganizationCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Organization
    fields = ['name', 'type']

    def test_func(self):
        return self.request.user.groups.filter(name='Administrators').exists()

    def form_valid(self, form):
        organization = form.save()
        organization.created_by = self.request.user
        organization.save()
        return super().form_valid(form)
