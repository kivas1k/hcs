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