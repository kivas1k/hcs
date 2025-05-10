from django.contrib import messages
from django.utils import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden
import zipfile
import os
from django.conf import settings
from io import BytesIO
from .models import Appeal, AppealDocument, Comment
from .forms import AppealForm, DocumentForm, StaffAppealForm, CommentForm, FeedbackForm


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
    search_query = request.GET.get('search', '')
    order_field = sort_mapping.get(filter_type, '-created_at')

    appeals = Appeal.objects.filter(author=request.user)

    if search_query:
        appeals = appeals.filter(title__icontains=search_query)
    else:
        if filter_type == 'title':
            appeals = sorted(
                appeals,
                key=lambda x: (not x.title.isdigit(), x.title.lower())
            )
        else:
            appeals = appeals.order_by(order_field)

    return render(request, 'appeals/my_appeals.html', {
        'appeals': appeals,
        'current_filter': filter_type,
        'search_query': search_query
    })

@login_required
def appeal_detail(request, appeal_id):
    if request.user.role in ['staff', 'admin']:
        appeal = get_object_or_404(Appeal, id=appeal_id)
    else:
        appeal = get_object_or_404(Appeal, id=appeal_id, author=request.user)

    documents = AppealDocument.objects.filter(appeal=appeal)
    comments = appeal.comments.all().order_by('created_at')
    comment_form = None
    feedback_form = None
    show_feedback_form = False

    if request.method == 'POST':
        if 'text' in request.POST:
            if request.user.is_authenticated and (request.user == appeal.author or request.user.is_staff):
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.appeal = appeal
                    comment.author = request.user
                    comment.save()
                    return redirect('appeals:appeal_detail', appeal_id=appeal_id)
            else:
                return HttpResponseForbidden("У вас нет прав оставлять комментарии")

        elif 'rating' in request.POST:
            if appeal.status == 'completed' and request.user == appeal.author and not appeal.rating:
                feedback_form = FeedbackForm(request.POST, instance=appeal)
                if feedback_form.is_valid():
                    feedback_form.save()
                    messages.success(request, 'Спасибо за вашу оценку!')
                    return redirect('appeals:appeal_detail', appeal_id=appeal_id)

    if request.user.is_authenticated and (request.user == appeal.author or request.user.is_staff):
        comment_form = CommentForm()

    if appeal.status == 'completed' and request.user == appeal.author and not appeal.rating:
        feedback_form = FeedbackForm(instance=appeal)
        show_feedback_form = True

    return render(request, 'appeals/appeal_detail.html', {
        'appeal': appeal,
        'documents': documents,
        'comments': comments,
        'comment_form': comment_form,
        'feedback_form': feedback_form,
        'show_feedback_form': show_feedback_form
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author:
        return HttpResponseForbidden("У вас нет прав удалять этот комментарий")

    if request.method == 'POST':
        appeal_id = comment.appeal.id
        comment.delete()
        messages.success(request, 'Комментарий успешно удален')
        return redirect('appeals:appeal_detail', appeal_id=appeal_id)

    return HttpResponseForbidden("Недопустимый метод запроса")

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author:
        return HttpResponseForbidden("У вас нет прав редактировать этот комментарий")

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            edited_comment = form.save(commit=False)
            edited_comment.updated_at = timezone.now()
            edited_comment.save()
            messages.success(request, 'Комментарий успешно обновлен')
            return redirect('appeals:appeal_detail', appeal_id=comment.appeal.id)

    return HttpResponseForbidden("Недопустимый метод запроса")

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
    sort_mapping = {
        'title': 'title',
        'id': 'id',
        'date': '-created_at'
    }

    filter_type = request.GET.get('filter_type', 'date')
    search_query = request.GET.get('search', '')
    order_field = sort_mapping.get(filter_type, '-created_at')

    appeals_qs = Appeal.objects.all()

    if search_query:
        appeals = appeals_qs.filter(title__icontains=search_query)
    else:
        if filter_type in ['id', 'date']:
            appeals = appeals_qs.order_by(order_field)
        elif filter_type == 'title':
            appeals = sorted(appeals_qs, key=lambda x: (not x.title.isdigit(), x.title.lower()))
        else:
            appeals = appeals_qs

    return render(request, 'appeals/staff_appeals.html', {
        'appeals': appeals,
        'appeals_count': appeals_qs.count(),
        'current_filter': filter_type,
        'search_query': search_query
    })

@staff_required
def staff_edit_appeal(request, appeal_id):
    appeal = get_object_or_404(Appeal, id=appeal_id)
    if request.method == 'POST':
        form = StaffAppealForm(request.POST, instance=appeal)
        if form.is_valid():
            if form.cleaned_data['employee_status'] == 'closed' and not appeal.closed_by:
                appeal.closed_by = request.user
                appeal.closed_at = timezone.now()
            form.save()
            messages.success(request, 'Изменения сохранены')
            return redirect('appeals:staff_appeals')
    else:
        form = StaffAppealForm(instance=appeal)

    return render(request, 'appeals/staff_edit_appeal.html', {
        'form': form,
        'appeal': appeal
    })

@staff_required
def staff_change_status(request, appeal_id, new_status):
    appeal = get_object_or_404(Appeal, id=appeal_id)
    user = request.user

    if request.method == 'POST':
        if new_status == 'in_progress':
            appeal.employee_status = 'in_progress'
            appeal.taken_by = user
            appeal.taken_at = timezone.now()
        elif new_status == 'closed':
            appeal.employee_status = 'closed'
            appeal.closed_by = user
            appeal.closed_at = timezone.now()
        else:
            appeal.employee_status = 'free'
            appeal.taken_by = None
            appeal.taken_at = None

        appeal.save()
        messages.success(request, 'Статус успешно обновлен')
        return redirect('appeals:staff_appeals')

    return HttpResponseForbidden("Недопустимый метод запроса")