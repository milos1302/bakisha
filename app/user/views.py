from django.views.generic import DetailView, ListView
from .models import Profile


class ProfileDetailView(DetailView):
    model = Profile


class PostListView(ListView):
    model = Profile
