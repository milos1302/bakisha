from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from common.utils.views import Operation, UserPassesTest
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
        return UserPassesTest.user_passes_test_with_message(self.request, Operation.CREATE, Organization)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('organization-update', kwargs={'slug': self.object.slug})


class OrganizationUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Organization
    fields = ['name', 'type', 'members', 'image', 'administrators']
    template_name = 'organization/organization_update.html'

    def test_func(self):
        return UserPassesTest.user_passes_test_with_message(self.request, Operation.UPDATE, Organization,
                                                            self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update {self.object.name}'
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['image'].required = False
        form.fields['administrators'].queryset = User.objects.filter(groups__name='Administrators')
        return form

    def form_valid(self, form):
        organization = self.get_object()
        created_by = organization.created_by
        is_created_by_in_members = form.cleaned_data.get('members').filter(pk=created_by.pk).exists()
        is_created_by_in_administrators = form.cleaned_data.get('administrators').filter(pk=created_by.pk).exists()
        if created_by and self.request.user != created_by and (
                not is_created_by_in_members or not is_created_by_in_administrators):
            # Prevent user that did not create organization to remove owner from the organization's group and/or administrators
            form.cleaned_data['administrators'] = form.cleaned_data.get('administrators').union(
                User.objects.filter(pk=created_by.pk))
            form.cleaned_data['members'] = form.cleaned_data.get('members').union(User.objects.filter(pk=created_by.pk))
            org_groups = '"administrators"' if not is_created_by_in_administrators else ''
            org_groups += ' and ' if not is_created_by_in_administrators and not is_created_by_in_members else ''
            org_groups += '"members"' if not is_created_by_in_members else ''
            messages.error(self.request, f'You do not have permission to remove owner of "{organization.name}" from {org_groups}.')
        return super().form_valid(form)


class OrganizationDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Organization
    success_url = '/organizations'

    def test_func(self):
        return UserPassesTest.user_passes_test_with_message(self.request, Operation.DELETE, Organization,
                                                            self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete {self.object.name}'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Organization "{self.get_object().name}" has been successfully deleted.')
        return super().delete(request, *args, **kwargs)
