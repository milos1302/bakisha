from django.contrib import admin
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from .models import Organization


class OrganizationAdminForm(ModelForm):
    class Meta:
        model = Organization
        exclude = []

    def clean(self):
        owner = self.cleaned_data.get('owner')
        if owner:
            owner_queryset = User.objects.filter(pk=self.cleaned_data.get('owner').pk)
            self.cleaned_data['administrators'] = self.cleaned_data['administrators'].union(owner_queryset)
            self.cleaned_data['members'] = self.cleaned_data['members'].union(owner_queryset)
        return self.cleaned_data


class OrganizationAdmin(admin.ModelAdmin):
    form = OrganizationAdminForm
    readonly_fields = ['created_by']

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
