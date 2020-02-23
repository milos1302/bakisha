from django.views.generic import DetailView, ListView
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Profile
from .forms import UserSignupForm


def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}! Your account has been created. You are now able to log in.')
            return redirect('/')
    else:
        form = UserSignupForm()
    return render(request, 'user/signup.html', {'form': form})


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
