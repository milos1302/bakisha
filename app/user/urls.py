from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='profile_list'),
    path('<int:pk>', views.ProfileDetailView.as_view(), name='profile_detail'),
]
