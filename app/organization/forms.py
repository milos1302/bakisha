from django import forms
from .models import Organization


class OrganizationFormBase(forms.ModelForm):
    owner = None

    def clean(self):
        data = super().clean()
        owner = self.owner if self.owner is not None else self.cleaned_data['owner']
        administrators = self.cleaned_data['administrators']
        if owner and owner not in administrators:
            raise forms.ValidationError(
                f'You can\'t remove user "{owner.username}" from the Administrators because they are the owner of the organization!')

        members = self.cleaned_data['members']
        if owner and owner not in members:
            raise forms.ValidationError(
                f'You can\'t remove user "{owner.username}" from the Members because they are the owner of the organization!')
        for administrator in administrators:
            if administrator not in members:
                raise forms.ValidationError(
                    f'User "{administrator.username}" must be a Member because they are an Administrator of the organization!')
        return data


class OrganizationAdminForm(OrganizationFormBase):
    class Meta:
        model = Organization
        fields = '__all__'
        widgets = {
            'administrators': forms.CheckboxSelectMultiple,
            'members': forms.CheckboxSelectMultiple
        }


class OrganizationUpdateForm(OrganizationFormBase):
    class Meta:
        model = Organization
        fields = ['name', 'type', 'image', 'members', 'administrators']
        widgets = {
            'members': forms.CheckboxSelectMultiple,
            'administrators': forms.CheckboxSelectMultiple
        }

    def set_owner(self, owner):
        self.owner = owner
