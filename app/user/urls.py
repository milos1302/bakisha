from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('', views.AccountListView.as_view(), name='account-list'),

    path('signup/', views.signup, name='user-signup'),
    path('login/', auth_view.LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='user/logout.html'), name='user-logout'),
    path('my-account/', views.my_account, name='my-account'),
    path('<slug:slug>/', views.AccountDetailView.as_view(), name='account-detail'),
    path('<slug:slug>/deactivate', views.AccountDeactivateView.as_view(), name='account-deactivate'),
]
