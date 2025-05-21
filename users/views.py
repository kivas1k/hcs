from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import user_passes_test
from .forms import RegisterForm, LoginForm, UserAdminForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from .models import Comment, User
from .forms import PublicCommentForm
from appeals.models import Tag, AppealStatus, Priority, EmployeeStatus
from django.views.decorators.http import require_POST

def home_view(request):
    comments = Comment.objects.filter(status='approved').order_by('-created_at')
    pending_comments = []

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'delete_comment':
            comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
            if comment.author == request.user or request.user.is_staff:
                comment.delete()
                messages.success(request, 'Комментарий успешно удален')
            return redirect('home')

        elif form_type == 'edit_comment':
            comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
            if comment.author == request.user:
                comment.text = request.POST.get('text')
                comment.status = 'pending'
                comment.is_edited = True
                comment.save()
                messages.success(request, 'Изменения отправлены на модерацию')
            return redirect('home')

        elif form_type == 'new_comment':
            form = PublicCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.save()
                messages.success(request, 'Комментарий отправлен на модерацию!')
            return redirect('home')

        elif 'action' in request.POST and request.user.is_staff:
            comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
            if request.POST.get('action') == 'approve':
                comment.status = 'approved'
                messages.success(request, 'Комментарий одобрен')
            elif request.POST.get('action') == 'reject':
                comment.status = 'rejected'
                messages.success(request, 'Комментарий отклонен')
            comment.save()
            return redirect('home')

    if request.user.is_staff:
        pending_comments = Comment.objects.filter(status='pending').order_by('created_at')

    return render(request, 'home.html', {
        'comments': comments,
        'pending_comments': pending_comments
    })

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

def admin_required(view_func):
    def check_admin(user):
        return user.is_authenticated and user.role == 'admin'
    return user_passes_test(check_admin)(view_func)

@admin_required
def admin_panel(request):
    return render(request, 'users/admin_panel.html')

@admin_required
def user_admin(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'users/user_list.html', {'users': users})

@admin_required
def edit_user_role(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserAdminForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Роль пользователя успешно обновлена')
            return redirect('users:user_admin')
    else:
        form = UserAdminForm(instance=user)
    return render(request, 'users/edit_user.html', {
        'form': form,
        'target_user': user
    })


@admin_required
def tag_admin(request):
    tags = Tag.objects.all().order_by('name')
    return render(request, 'users/tag_list.html', {'tags': tags})


@admin_required
def create_tag(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Tag.objects.create(name=name)
            messages.success(request, 'Тег успешно создан')
            return redirect('users:tag_admin')
    return render(request, 'users/tag_form.html')


@admin_required
def edit_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        tag.name = request.POST.get('name')
        tag.save()
        messages.success(request, 'Тег обновлен')
        return redirect('users:tag_admin')
    return render(request, 'users/tag_form.html', {'tag': tag})


@require_POST
@admin_required
def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    messages.success(request, 'Тег удален')
    return redirect('users:tag_admin')


# Общие функции для управления статусами и приоритетами
@admin_required
def status_admin(request, model_type):
    model_map = {
        'appealstatus': (AppealStatus, 'статусы обращений'),
        'priority': (Priority, 'приоритеты'),
        'employeestatus': (EmployeeStatus, 'статусы сотрудников')
    }
    model_class, verbose_name = model_map[model_type]
    objects = model_class.objects.all().order_by('code')
    return render(request, 'users/status_list.html', {
        'objects': objects,
        'model_name': verbose_name,
        'model_type': model_type
    })


@admin_required
def create_status(request, model_type):
    model_map = {
        'appealstatus': (AppealStatus, 'статус обращения'),
        'priority': (Priority, 'приоритет'),
        'employeestatus': (EmployeeStatus, 'статус сотрудника')
    }
    model_class, verbose_name = model_map[model_type]

    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        if name and code:
            model_class.objects.create(name=name, code=code)
            messages.success(request, f'{verbose_name.capitalize()} создан')
            return redirect('users:status_admin', model_type=model_type)

    return render(request, 'users/status_form.html', {
        'model_type': model_type,
        'verbose_name': verbose_name
    })


@admin_required
def edit_status(request, model_type, pk):
    model_map = {
        'appealstatus': AppealStatus,
        'priority': Priority,
        'employeestatus': EmployeeStatus
    }
    model_class = model_map[model_type]
    obj = get_object_or_404(model_class, pk=pk)

    if request.method == 'POST':
        obj.name = request.POST.get('name')
        obj.code = request.POST.get('code')
        obj.save()
        messages.success(request, 'Изменения сохранены')
        return redirect('users:status_admin', model_type=model_type)

    return render(request, 'users/status_form.html', {
        'object': obj,
        'model_type': model_type
    })


@require_POST
@admin_required
def delete_status(request, model_type, pk):
    model_map = {
        'appealstatus': AppealStatus,
        'priority': Priority,
        'employeestatus': EmployeeStatus
    }
    model_class = model_map[model_type]
    obj = get_object_or_404(model_class, pk=pk)
    obj.delete()
    messages.success(request, 'Удалено успешно')
    return redirect('users:status_admin', model_type=model_type)