from django import template

register = template.Library()


@register.filter(name='is_org_admin')
def is_org_admin(user, org=None):
    """
    If org (Organization) is provided, it checks if the user
    is one of the org's administrators. Returns True if they are
    and False otherwise.
    If org is NOT provided, it checks if the user is administrator
    of any organization. Returns True if they are and False otherwise.
    """
    if org:
        return org.administrators.filter(id=user.id).exists()
    return user.administrating_organizations.first() is not None
