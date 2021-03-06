from django.shortcuts import render


def home(request):
    return render(request, 'pages/home.html', {'title': 'Home'})


def handler403(request, exception=None):
    return render(request, 'pages/403.html', {'title': 'Permission Denied'})
