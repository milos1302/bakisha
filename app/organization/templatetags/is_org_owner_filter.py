from django import template

register = template.Library()


@register.filter(name='is_org_owner')
def is_org_owner(user, org):
    if org.created_by:
        return org.created_by == user
    return False
