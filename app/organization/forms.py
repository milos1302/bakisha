from django import forms
from django.contrib.auth.models import User
from .models import Organization

class OrganizationAdminForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        widgets = {
            'administrators': forms.CheckboxSelectMultiple,
            'members': forms.CheckboxSelectMultiple
        }

    def clean(self):
        owner = self.cleaned_data.get('owner')
        if owner:
            owner_queryset = User.objects.filter(pk=self.cleaned_data.get('owner').pk)
            self.cleaned_data['administrators'] = self.cleaned_data['administrators'].union(owner_queryset)
            self.cleaned_data['members'] = self.cleaned_data['members'].union(owner_queryset)
        return self.cleaned_data

class OrganizationUpdateForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'type', 'image', 'members', 'administrators']
        widgets = {
            'members': forms.CheckboxSelectMultiple,
            'administrators': forms.CheckboxSelectMultiple
        }
