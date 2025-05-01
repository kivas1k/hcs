from django.urls import path
from . import views

app_name = 'appeals'

urlpatterns = [
    path('create/', views.create_appeal, name='create_appeal'),
    path('mine/', views.my_appeals, name='my_appeals'),
    path('<int:appeal_id>/', views.appeal_detail, name='appeal_detail'),
    path('<int:appeal_id>/edit/', views.edit_appeal, name='edit_appeal'),
    path('<int:appeal_id>/delete/', views.delete_appeal, name='delete_appeal'),
    path('document/<int:document_id>/delete/', views.delete_document, name='delete_document'),
    path('<int:appeal_id>/download/', views.download_all_documents, name='download_all_documents'),
    path('staff/all/', views.staff_appeals, name='staff_appeals'),
    path('staff/<int:appeal_id>/edit-tags/', views.staff_edit_tags, name='staff_edit_tags'),
]