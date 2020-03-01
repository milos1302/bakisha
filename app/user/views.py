from django.views.generic import DetailView, ListView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from common.utils.user_passes_test import UserPassesTest
from common.enums import CrudOperations
from common.utils.messages import Messenger
from .models import Account
from .forms import UserSignupForm, UserUpdateForm, AccountUpdateForm


def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}! Your account has been created. You are now able to log in.')
            return redirect('user-login')
    else:
        form = UserSignupForm()
    return render(request, 'user/signup.html', {'form': form})


@login_required
def my_account(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        account_form = AccountUpdateForm(request.POST, request.FILES, instance=request.user.account)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('my-account')
    else:
        user_form = UserUpdateForm(instance=request.user)
        account_form = AccountUpdateForm(instance=request.user.account)

    context = {
        'account': request.user.account,
        'user_form': user_form,
        'account_form': account_form
    }

    return render(request, 'user/my_account.html', context)


class AccountDetailView(DetailView):
    model = Account

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = context['account'].user.username
        context['title'] = f"{username}'s account"
        return context


class AccountListView(ListView):
    model = Account
    extra_context = {'title': 'Players'}

    def get_queryset(self):
        return Account.objects.filter(user__is_active=True)


class AccountDeactivateView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Account
    success_url = '/'
    template_name_suffix = '_confirm_deactivate'

    def test_func(self):
        return UserPassesTest.user_passes_test_with_message(self.request, CrudOperations.DELETE,
                                                            Account, self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete {self.get_object().user.username}'
        return context

    def delete(self, request, *args, **kwargs):
        account = self.get_object()
        account.user.is_active = False
        account.user.save()
        Messenger.crud_success(self.request, CrudOperations.DELETE, account)
        return HttpResponseRedirect(self.success_url)
