from django import forms
from .models import Organization


class OrganizationUpdateForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'type', 'image', 'members', 'administrators']
        widgets = {
            'members': forms.CheckboxSelectMultiple,
            'administrators': forms.CheckboxSelectMultiple
        }
