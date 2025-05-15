from django.contrib import admin
from .models import Tag, AppealStatus, Priority, EmployeeStatus, Appeal, AppealDocument, Comment

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(AppealStatus)
class AppealStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(EmployeeStatus)
class EmployeeStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

class AppealDocumentInline(admin.TabularInline):
    model = AppealDocument
    extra = 0

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'priority', 'employee_status', 'created_at')
    list_filter = ('status', 'priority', 'employee_status')
    search_fields = ('title', 'description')
    inlines = [AppealDocumentInline, CommentInline]
    filter_horizontal = ('tags',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('appeal', 'author', 'created_at')
    search_fields = ('text',)