from django.views.generic import DetailView, ListView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from common.utils.user_passes_test import UserPassesTest
from common.enums import CrudOperations
from common.utils.messages import Messenger
from .models import Profile
from .forms import UserSignupForm, UserUpdateForm, ProfileUpdateForm


def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}! Your account has been created. You are now able to log in.')
            return redirect('user-login')
    else:
        form = UserSignupForm()
    return render(request, 'user/signup.html', {'form': form})


@login_required
def my_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('my-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'profile': request.user.profile,
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'user/my_profile.html', context)


class ProfileDetailView(DetailView):
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = context['profile'].user.username
        context['title'] = f"{username}'s profile"
        return context


class ProfileListView(ListView):
    model = Profile
    extra_context = {'title': 'Players'}

    def get_queryset(self):
        return Profile.objects.filter(user__is_active=True)


class ProfileDeactivateView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    success_url = '/'
    template_name_suffix = '_confirm_deactivate'

    def test_func(self):
        return UserPassesTest.user_passes_test_with_message(self.request, CrudOperations.DELETE,
                                                            Profile, self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete {self.get_object().user.username}'
        return context

    def delete(self, request, *args, **kwargs):
        profile = self.get_object()
        profile.user.is_active = False
        profile.user.save()
        Messenger.crud_success(self.request, CrudOperations.DELETE, profile)
        return HttpResponseRedirect(self.success_url)
