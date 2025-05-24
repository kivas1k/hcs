from django import forms
from .models import Appeal, Tag, Comment, AppealStatus, Priority, EmployeeStatus
from django.core.validators import RegexValidator

class FeedbackForm(forms.ModelForm):
    RATING_CHOICES = [(i, '★' * i) for i in range(1, 6)]

    rating = forms.ChoiceField(
        label='Оценка',
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        required=True
    )
    feedback_comment = forms.CharField(
        label='Комментарий',
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False
    )

    class Meta:
        model = Appeal
        fields = ['rating', 'feedback_comment']

class AppealForm(forms.ModelForm):
    title = forms.CharField(
        label='Заголовок',
        min_length=5,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите заголовок обращения'
        }),
        error_messages={
            'min_length': 'Минимум 5 символов в заголовке',
            'required': 'Это поле обязательно'
        }
    )
    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Подробно опишите вашу проблему'
        }),
        min_length=10,
        max_length=1000,
        error_messages={
            'min_length': 'Минимум 10 символов в описании'
        }
    )
    full_name = forms.CharField(
        label='ФИО',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иванов Иван Иванович',
            'pattern': '[а-яА-ЯёЁa-zA-Z\\s\\-]+',
            'title': 'Только буквы, пробелы и дефисы'
        }),
        validators=[
            RegexValidator(
                regex=r'^[а-яА-ЯёЁa-zA-Z\s\-]+$',
                message="Недопустимые символы в ФИО"
            )
        ]
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+79999999999',
            'pattern': r'\+7\d{10}',
            'title': 'Формат: +7XXXXXXXXXX'
        }),
        required=False,
        error_messages={
            'invalid': 'Неверный формат номера'
        }
    )
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
        }),
        max_length=300
    )

    class Meta:
        model = Appeal
        fields = ['title', 'full_name', 'phone', 'address', 'description', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.phone:
            self.fields['phone'].initial = user.phone

class StaffAppealForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=AppealStatus.objects.all(),
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    priority = forms.ModelChoiceField(
        queryset=Priority.objects.all(),
        label='Приоритет',
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

class ChangeEmployeeStatusForm(forms.ModelForm):
    class Meta:
        model = Appeal
        fields = ['employee_status']
        widgets = {
            'employee_status': forms.HiddenInput()
        }