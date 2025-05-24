from django.contrib import admin
from .models import FAQCategory, FAQItem

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'author')
    list_editable = ('order',)
    search_fields = ('name',)
    fields = ('name', 'order', 'author')

    def save_model(self, request, obj, form, change):
        if not change and request.user.is_authenticated:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'author')
    list_filter = ('category',)
    list_editable = ('order',)
    search_fields = ('question', 'answer')
    fields = ('category', 'question', 'answer', 'order', 'author')

    def save_model(self, request, obj, form, change):
        if not change and request.user.is_authenticated:
            obj.author = request.user
        super().save_model(request, obj, form, change)
