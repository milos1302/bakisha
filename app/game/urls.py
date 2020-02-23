from django.urls import path
from . import views

urlpatterns = [
    path('', views.GameListView.as_view(), name='game-list'),
    path('<slug:slug>/', views.GameDetailView.as_view(), name='game-detail'),
    path('create/', views.GameCreateView.as_view(), name='game-create'),
]
