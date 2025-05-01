from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import UserChangeForm

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
        widget=forms.TextInput(attrs={
            'placeholder': 'Придумайте логин',
            'class': 'form-control'
        }),
        help_text=''
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите ваш email',
            'class': 'form-control'
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
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': PhoneInput(),
        }