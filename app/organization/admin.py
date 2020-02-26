from django.contrib import admin
from django.contrib.auth.models import User
from .models import Organization


class OrganizationAdmin(admin.ModelAdmin):

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Prevent adding non-administrators to organization's administrators.
        Only users in 'Administrators' group can be added as organization's
        administrators.
        """
        if db_field.name == 'administrators':
            kwargs['queryset'] = User.objects.filter(groups__name='Administrators')
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Organization, OrganizationAdmin)
