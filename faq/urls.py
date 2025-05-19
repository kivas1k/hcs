from django.urls import path
from . import views

app_name = 'faq'

urlpatterns = [
    path('', views.faq_view, name='faq'),
    path('category/create/', views.create_category, name='create_category'),
    path('category/update/<int:pk>/', views.update_category, name='update_category'),
    path('category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('question/create/', views.create_question, name='create_question'),
    path('question/update/<int:pk>/', views.update_question, name='update_question'),
    path('question/delete/<int:pk>/', views.delete_question, name='delete_question'),
]