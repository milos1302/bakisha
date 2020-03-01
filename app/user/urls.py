from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='profile-list'),

    path('signup/', views.signup, name='user-signup'),
    path('login/', auth_view.LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='user/logout.html'), name='user-logout'),
    path('my-profile/', views.my_profile, name='my-profile'),
    path('<slug:slug>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('<slug:slug>/deactivate', views.ProfileDeactivateView.as_view(), name='profile-deactivate'),
]
