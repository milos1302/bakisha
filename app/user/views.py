from django.views.generic import DetailView
from .models import Profile


class ProfileDetailView(DetailView):
    model = Profile
