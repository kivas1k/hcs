from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Comment
from .forms import RegisterForm


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = RegisterForm
    list_display = ('username', 'email', 'phone', 'role', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Права доступа', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser'),
        }),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'phone',
                'password1',
                'password2',
                'role',
                'is_staff',
                'is_active'
            )}
         ),
    )

    actions = ['make_staff', 'make_user']

    def make_staff(self, request, queryset):
        queryset.update(role='staff', is_staff=True)

    make_staff.short_description = "Назначить выбранных сотрудниками"

    def make_user(self, request, queryset):
        queryset.update(role='user', is_staff=False)

    make_user.short_description = "Назначить выбранных обычными пользователями"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('text', 'author__username')
    list_editable = ('status',)
    raw_id_fields = ('author',)


admin.site.register(User, CustomUserAdmin)