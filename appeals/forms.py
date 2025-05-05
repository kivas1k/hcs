from django import forms
from .models import Appeal, Tag, Comment

class AppealForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tags-checkbox'}),
        required=False,
        label='Теги'
    )

    address = forms.CharField(
        label='Адрес проживания',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: г. Москва, ул. Ленина, д. 15, кв. 42'
        })
    )

    full_name = forms.CharField(
        label='ФИО',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иванов Иван Иванович'
        })
    )

    class Meta:
        model = Appeal
        fields = ['title', 'full_name', 'address', 'description', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
            }),
        }

class StaffAppealForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tags-checkbox'}),
        required=False,
        label='Теги'
    )

    class Meta:
        model = Appeal
        fields = ['tags']

class DocumentForm(forms.Form):
    files = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Прикрепите документы',
        required=False
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите ваш комментарий...'
            })
        }


class StaffAppealForm(forms.ModelForm):
    status = forms.ChoiceField(
        label='Статус',
        choices=Appeal.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    priority = forms.ChoiceField(
        label='Приоритет',
        choices=Appeal.PRIORITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tags-checkbox'}),
        required=False,
        label='Теги'
    )

    class Meta:
        model = Appeal
        fields = ['status', 'priority', 'tags']