from django import forms
from .models import Appeal

class AppealForm(forms.ModelForm):
    class Meta:
        model = Appeal
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class DocumentForm(forms.Form):
    files = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Прикрепите документы',
        required=False
    )