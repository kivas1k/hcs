from django.contrib import admin
from .models import FAQCategory, FAQItem

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    search_fields = ('name',)

@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order')
    list_filter = ('category',)
    list_editable = ('order',)
    search_fields = ('question', 'answer')
    fieldsets = (
        (None, {
            'fields': ('category', 'question', 'answer', 'order')
        }),
    )