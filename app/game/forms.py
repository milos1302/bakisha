from django import forms
from .models import Game
from organization.models import Organization


class GameCreateForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'organization']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['organization'].queryset = Organization.objects.filter(administrators=user.id)
