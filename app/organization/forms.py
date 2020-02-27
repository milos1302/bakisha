from django import forms
from .models import Organization

class OrganizationAdminForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        widgets = {
            'administrators': forms.CheckboxSelectMultiple,
            'members': forms.CheckboxSelectMultiple
        }

    def clean_administrators(self):
        owner = self.cleaned_data.get('owner')
        administrators = self.cleaned_data['administrators']
        if owner and owner not in administrators:
            raise forms.ValidationError('Owner must be an administrator of the organization!')
        return administrators

    def clean_members(self):
        owner = self.cleaned_data.get('owner')
        members = self.cleaned_data['members']
        if owner and owner not in members:
            raise forms.ValidationError('Owner must be a member of the organization!')
        return members

class OrganizationUpdateForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'type', 'image', 'members', 'administrators']
        widgets = {
            'members': forms.CheckboxSelectMultiple,
            'administrators': forms.CheckboxSelectMultiple
        }
