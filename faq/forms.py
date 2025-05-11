from django import forms
from .models import FAQCategory, FAQItem

class FAQCategoryForm(forms.ModelForm):
    class Meta:
        model = FAQCategory
        fields = ['name', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'})
        }

class FAQItemForm(forms.ModelForm):
    class Meta:
        model = FAQItem
        fields = ['category', 'question', 'answer', 'order']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'})
        }