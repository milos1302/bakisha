from django import template
from user.models import Account

register = template.Library()


@register.filter(name='has_paid_subscription')
def has_paid_subscription(user):
    return user.account.subscription == Account.PAID
