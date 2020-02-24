from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrganizationListView.as_view(), name='organization-list'),
    path('<slug:slug>/', views.OrganizationDetailView.as_view(), name='organization-detail'),
]
