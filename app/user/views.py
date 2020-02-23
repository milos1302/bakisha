from django.views.generic import DetailView, ListView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Profile, Organization
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


class OrganizationDetailView(DetailView):
    model = Organization


class OrganizationListView(ListView):
    model = Organization
