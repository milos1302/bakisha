from django import template

register = template.Library()


@register.filter(name='is_org_admin')
def is_org_admin(user):
    return user.administrating_organizations.first() is not None
