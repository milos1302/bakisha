from django import forms
from django.contrib.auth.models import User
from common.enums import ValidationErrors
from common.utils.messages import Messenger
from .models import Organization


class OrganizationFormBase(forms.ModelForm):
    owner = None

    def clean(self):
        data = super().clean()
        owner = self.owner if self.owner is not None else self.cleaned_data['owner']
        administrators = self.cleaned_data.get('administrators')
        members = self.cleaned_data['members']

        if administrators is not None:
            if owner and owner not in administrators:
                Messenger.form_invalid(ValidationErrors.REMOVE_OWNER_FROM_ADMINS, owner.username)
            for administrator in administrators:
                if administrator not in members:
                    Messenger.form_invalid(ValidationErrors.REMOVE_ADMIN_FROM_MEMBERS, administrator.username)

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
        fields = ['name', 'type', 'image', 'members']
        widgets = {
            'members': forms.CheckboxSelectMultiple,
        }

    def __init__(self, owner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.owner = owner


class OrganizationOwnerUpdateForm(OrganizationUpdateForm):
    class Meta(OrganizationUpdateForm.Meta):
        fields = ['name', 'type', 'image', 'members', 'administrators']
        widgets = {
            'members': forms.CheckboxSelectMultiple,
            'administrators': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['administrators'].queryset = User.objects.filter(groups__name='Administrators')
