from django.urls import path
from . import views

app_name = 'faq'

urlpatterns = [
    path('', views.faq_view, name='faq'),
    path('category/add/', views.edit_category, name='add_category'),
    path('category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('question/add/', views.edit_question, name='add_question'),
    path('question/edit/<int:pk>/', views.edit_question, name='edit_question'),
    path('question/delete/<int:pk>/', views.delete_question, name='delete_question'),
]