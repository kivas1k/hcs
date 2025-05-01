from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
import zipfile
import os
from django.conf import settings
from io import BytesIO
from .models import Appeal, AppealDocument
from .forms import AppealForm, DocumentForm, StaffAppealForm

def staff_required(view_func=None):
    def check_staff(user):
        return user.is_authenticated and user.role in ['staff', 'admin']
    decorator = user_passes_test(
        check_staff,
        login_url='/users/login/',
        redirect_field_name=None
    )
    return decorator(view_func) if view_func else decorator

@login_required
def create_appeal(request):
    if request.method == 'POST':
        form = AppealForm(request.POST)
        document_form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            appeal = form.save(commit=False)
            appeal.author = request.user
            appeal.save()
            form.save_m2m()

            files = request.FILES.getlist('files')
            for f in files:
                AppealDocument.objects.create(appeal=appeal, file=f)

            return redirect('home')

    else:
        form = AppealForm()
        document_form = DocumentForm()

    return render(request, 'appeals/create_appeal.html', {
        'form': form,
        'document_form': document_form
    })

@login_required
def my_appeals(request):
    sort_mapping = {
        'title': 'title',
        'id': 'id',
        'date': '-created_at'
    }

    filter_type = request.GET.get('filter_type', 'date')
    order_field = sort_mapping.get(filter_type, '-created_at')

    appeals = Appeal.objects.filter(author=request.user).order_by(order_field)

    if filter_type == 'title':
        appeals = sorted(
            appeals,
            key=lambda x: (not x.title.isdigit(), x.title.lower())
        )

    return render(request, 'appeals/my_appeals.html', {
        'appeals': appeals,
        'current_filter': filter_type
    })


@login_required
def appeal_detail(request, appeal_id):
    if request.user.role in ['staff', 'admin']:
        appeal = get_object_or_404(Appeal, id=appeal_id)
    else:

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

@login_required
def download_all_documents(request, appeal_id):

    if request.user.role in ['staff', 'admin']:
        appeal = get_object_or_404(Appeal, id=appeal_id)
    else:
        appeal = get_object_or_404(Appeal, id=appeal_id, author=request.user)

    documents = AppealDocument.objects.filter(appeal=appeal)

    if not documents:
        messages.warning(request, 'Нет прикрепленных документов')
        return redirect('appeals:appeal_detail', appeal_id=appeal_id)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for document in documents:
            file_path = os.path.join(settings.MEDIA_ROOT, document.file.name)
            if os.path.exists(file_path):
                zip_file.write(file_path, os.path.basename(document.file.name))

    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="appeal_{appeal_id}_documents.zip"'
    return response

@staff_required
def staff_appeals(request):
    appeals = Appeal.objects.all().order_by('-created_at')
    return render(request, 'appeals/staff_appeals.html', {
        'appeals': appeals
    })

@staff_required
def staff_edit_tags(request, appeal_id):
    appeal = get_object_or_404(Appeal, id=appeal_id)
    if request.method == 'POST':
        form = StaffAppealForm(request.POST, instance=appeal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Теги обновлены')
            return redirect('appeals:staff_appeals')
    else:
        form = StaffAppealForm(instance=appeal)

    return render(request, 'appeals/staff_edit_tags.html', {
        'form': form,
        'appeal': appeal
    })