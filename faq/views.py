from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import FAQCategory, FAQItem
from .forms import FAQCategoryForm, FAQItemForm

def admin_required(view_func):
    def check_admin(user):
        return user.is_authenticated and user.role == 'admin'
    return user_passes_test(check_admin)(view_func)

def faq_view(request):
    categories = FAQCategory.objects.prefetch_related('questions').all()
    return render(request, 'faq/faq.html', {
        'categories': categories,
        'is_admin': request.user.is_authenticated and request.user.role == 'admin'
    })

@admin_required
def create_category(request):
    if request.method == 'POST':
        form = FAQCategoryForm(request.POST, user=request.user)
        if form.is_valid():
            category = form.save(commit=False)
            category.author = request.user
            category.save()
            return redirect('faq:faq')
    else:
        form = FAQCategoryForm(user=request.user)
    return render(request, 'faq/edit_category.html', {'form': form})

@admin_required
def update_category(request, pk):
    category = get_object_or_404(FAQCategory, pk=pk)
    if request.method == 'POST':
        form = FAQCategoryForm(request.POST, instance=category, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('faq:faq')
    else:
        form = FAQCategoryForm(instance=category, user=request.user)
    return render(request, 'faq/edit_category.html', {'form': form})

@admin_required
def delete_category(request, pk):
    category = get_object_or_404(FAQCategory, pk=pk)
    category.delete()
    return redirect('faq:faq')

@admin_required
def create_question(request):
    if request.method == 'POST':
        form = FAQItemForm(request.POST, user=request.user)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('faq:faq')
    else:
        form = FAQItemForm(user=request.user)
    return render(request, 'faq/edit_question.html', {'form': form})

@admin_required
def update_question(request, pk):
    question = get_object_or_404(FAQItem, pk=pk)
    if request.method == 'POST':
        form = FAQItemForm(request.POST, instance=question, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('faq:faq')
    else:
        form = FAQItemForm(instance=question, user=request.user)
    return render(request, 'faq/edit_question.html', {'form': form})

@admin_required
def delete_question(request, pk):
    question = get_object_or_404(FAQItem, pk=pk)
    question.delete()
    return redirect('faq:faq')