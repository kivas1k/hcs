from django import forms
from .models import FAQCategory, FAQItem
from users.models import User
from django.core.validators import RegexValidator

class FAQCategoryForm(forms.ModelForm):
    name = forms.CharField(
        label='Название категории',
        min_length=3,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': '[а-яА-ЯёЁa-zA-Z0-9\\s\\-_]+',
            'title': 'Только буквы, цифры, пробелы, дефисы и подчеркивания'
        }),
        error_messages={
            'min_length': 'Минимум 3 символа',
            'max_length': 'Максимум 100 символов'
        }
    )
    order = forms.IntegerField(
        label='Порядок',
        min_value=0,
        max_value=1000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '1000'
        })
    )
    author = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = FAQCategory
        fields = ['name', 'order', 'author']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['author'].initial = user

class FAQItemForm(forms.ModelForm):
    question = forms.CharField(
        label='Вопрос',
        min_length=10,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': '[а-яА-ЯёЁa-zA-Z0-9\\s\\-\\?\\.!,]+',
            'title': 'Допустимы буквы, цифры и основные знаки препинания'
        }),
        error_messages={
            'min_length': 'Минимум 10 символов',
            'max_length': 'Максимум 255 символов'
        }
    )
    answer = forms.CharField(
        label='Ответ',
        min_length=20,
        max_length=5000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'data-maxlength': '5000'
        }),
        error_messages={
            'min_length': 'Минимум 20 символов',
            'max_length': 'Максимум 5000 символов'
        }
    )
    order = forms.IntegerField(
        label='Порядок',
        min_value=0,
        max_value=1000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '1000'
        })
    )
    author = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = FAQItem
        fields = ['category', 'question', 'answer', 'order', 'author']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['author'].initial = user