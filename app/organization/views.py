from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Organization


class OrganizationDetailView(DetailView):
    model = Organization


class OrganizationListView(ListView):
    model = Organization


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    fields = ['name', 'type']

    def form_valid(self, form):
        organization = form.save()
        organization.created_by = self.request.user
        organization.save()
        return super().form_valid(form)
