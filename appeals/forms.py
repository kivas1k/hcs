from django import forms
from .models import Appeal, Tag, Comment


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
    employee_status = forms.ChoiceField(
        label='Статус для сотрудников',
        choices=Appeal.EMPLOYEE_STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Appeal
        fields = ['status', 'priority', 'tags', 'employee_status']


class ChangeEmployeeStatusForm(forms.Form):
    status = forms.ChoiceField(
        choices=Appeal.EMPLOYEE_STATUS_CHOICES,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Appeal
        fields = ['status', 'priority', 'tags']