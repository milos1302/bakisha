from django.urls import path
from . import views

urlpatterns = [
    path('', views.GameListView.as_view(), name='game-list'),
    path('create/', views.GameCreateView.as_view(), name='game-create'),
    path('<slug:slug>/', views.GameDetailView.as_view(), name='game-detail'),
    path('<slug:slug>/update', views.GameUpdateView.as_view(), name='game-update'),
    path('<slug:slug>/delete', views.GameDeleteView.as_view(), name='game-delete'),
]
