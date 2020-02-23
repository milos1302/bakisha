from django.views.generic import DetailView, ListView
from .models import Profile


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
