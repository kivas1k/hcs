from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appeal, AppealDocument
from .forms import AppealForm, DocumentForm
@login_required
def create_appeal(request):
    if request.method == 'POST':
        appeal_form = AppealForm(request.POST)
        document_form = DocumentForm(request.POST, request.FILES)

        if appeal_form.is_valid():
            appeal = appeal_form.save(commit=False)
            appeal.author = request.user
            appeal.save()

            files = request.FILES.getlist('files')
            for f in files:
                AppealDocument.objects.create(appeal=appeal, file=f)

            return redirect('home')

    else:
        appeal_form = AppealForm()
        document_form = DocumentForm()

    return render(request, 'appeals/create_appeal.html', {
        'appeal_form': appeal_form,
        'document_form': document_form
    })

@login_required
def my_appeals(request):
    appeals = Appeal.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'appeals/my_appeals.html', {'appeals': appeals})

@login_required
def appeal_detail(request, appeal_id):
    appeal = get_object_or_404(Appeal, id=appeal_id, author=request.user)
    documents = AppealDocument.objects.filter(appeal=appeal)
    return render(request, 'appeals/appeal_detail.html', {
        'appeal': appeal,
        'documents': documents
    })


@login_required
def edit_appeal(request, appeal_id):
    appeal = get_object_or_404(Appeal, id=appeal_id, author=request.user)

    if request.method == 'POST':
        appeal_form = AppealForm(request.POST, instance=appeal)
        document_form = DocumentForm(request.POST, request.FILES)

        if appeal_form.is_valid():
            appeal = appeal_form.save()

            # Добавление новых файлов
            files = request.FILES.getlist('files')
            for f in files:
                AppealDocument.objects.create(appeal=appeal, file=f)

            messages.success(request, 'Обращение успешно обновлено')
            return redirect('appeals:appeal_detail', appeal_id=appeal.id)
    else:
        appeal_form = AppealForm(instance=appeal)
        document_form = DocumentForm()

    documents = AppealDocument.objects.filter(appeal=appeal)
    return render(request, 'appeals/edit_appeal.html', {
        'appeal_form': appeal_form,
        'document_form': document_form,
        'documents': documents,
        'appeal': appeal
    })


@login_required
def delete_appeal(request, appeal_id):
    appeal = get_object_or_404(Appeal, id=appeal_id, author=request.user)

    if request.method == 'POST':
        appeal.delete()
        messages.success(request, 'Обращение успешно удалено')
        return redirect('appeals:my_appeals')

    return redirect('appeals:appeal_detail', appeal_id=appeal.id)


@login_required
def delete_document(request, document_id):
    document = get_object_or_404(AppealDocument, id=document_id, appeal__author=request.user)
    document.delete()
    return redirect('appeals:edit_appeal', appeal_id=document.appeal.id)