from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import FAQCategory, FAQItem
from .forms import FAQCategoryForm, FAQItemForm

def staff_required(view_func):
    def check_staff(user):
        return user.is_authenticated and user.role in ['staff', 'admin']
    return user_passes_test(check_staff)(view_func)

def faq_view(request):
    categories = FAQCategory.objects.prefetch_related('questions').all()
    return render(request, 'faq/faq.html', {
        'categories': categories,
        'is_staff': request.user.is_authenticated and request.user.is_staff
    })

@staff_required
def edit_category(request, pk=None):
    if pk:
        category = get_object_or_404(FAQCategory, pk=pk)
    else:
        category = None

    if request.method == 'POST':
        form = FAQCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('faq:faq')
    else:
        form = FAQCategoryForm(instance=category)

    return render(request, 'faq/edit_category.html', {'form': form})

@staff_required
def edit_question(request, pk=None):
    if pk:
        question = get_object_or_404(FAQItem, pk=pk)
    else:
        question = None

    if request.method == 'POST':
        form = FAQItemForm(request.POST, instance=question)
        if form.is_valid():
            instance = form.save(commit=False)
            if not instance.created_by:
                instance.created_by = request.user
            instance.save()
            return redirect('faq:faq')
    else:
        form = FAQItemForm(instance=question)

    return render(request, 'faq/edit_question.html', {'form': form})

@staff_required
def delete_category(request, pk):
    category = get_object_or_404(FAQCategory, pk=pk)
    category.delete()
    return redirect('faq:faq')

@staff_required
def delete_question(request, pk):
    question = get_object_or_404(FAQItem, pk=pk)
    question.delete()
    return redirect('faq:faq')