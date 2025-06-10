from django import forms
from .models import Comment, User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator

class PhoneInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({
            'placeholder': '+79999999999',
            'pattern': r'\+7\d{10}',
            'title': 'Введите номер в формате +79999999999',
            'class': 'form-control'
        })
        super().__init__(*args, **kwargs)

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        min_length=4,
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'Придумайте логин (4-30 символов)',
            'class': 'form-control',
            'pattern': r'[\w.@+-]+'
        }),
        help_text='Только буквы, цифры и @/./+/-/_',
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message="Недопустимые символы в логине"
            )
        ]
    )

    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите ваш email',
            'class': 'form-control',
            'maxlength': '254'
        }),
        required=True
    )

    phone = forms.CharField(
        label='Телефон',
        widget=PhoneInput(),
        help_text=''
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Создайте пароль',
            'class': 'form-control'
        }),
        help_text=''
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Повторите пароль',
            'class': 'form-control'
        }),
        help_text=''
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ваш логин',
            'class': 'form-control'
        })
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль',
            'class': 'form-control'
        })
    )

class EditProfileForm(UserChangeForm):
    first_name = forms.CharField(
        label='Имя',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': '[а-яА-ЯёЁa-zA-Z\\s\\-]+'
        })
    )

    last_name = forms.CharField(
        label='Фамилия',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': '[а-яА-ЯёЁa-zA-Z\\s\\-]+'
        })
    )

    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'maxlength': '254'
        })
    )

    phone = forms.CharField(
        label='Телефон',
        widget=PhoneInput()
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': PhoneInput(),
        }

class PublicCommentForm(forms.ModelForm):
    text = forms.CharField(
        label='Комментарий',
        min_length=10,
        max_length=1000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Оставьте ваш комментарий (10-1000 символов)',
            'maxlength': '1000'
        })
    )

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Оставьте ваш комментарий...'
            })
        }

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role', 'is_active']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'role': 'Роль пользователя',
            'is_active': 'Активный аккаунт'
        }