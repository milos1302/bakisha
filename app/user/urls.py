from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='profile-list'),
    path('<int:pk>', views.ProfileDetailView.as_view(), name='profile-detail'),
]
