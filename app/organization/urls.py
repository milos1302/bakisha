from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrganizationListView.as_view(), name='organization-list'),
    path('create/', views.OrganizationCreateView.as_view(), name='organization-create'),
    path('<slug:slug>/', views.OrganizationDetailView.as_view(), name='organization-detail'),
    path('<slug:slug>/update', views.OrganizationUpdateView.as_view(), name='organization-update'),
    path('<slug:slug>/delete', views.OrganizationDeleteView.as_view(), name='organization-delete'),
]
