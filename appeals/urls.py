from django.urls import path
from . import views

app_name = 'appeals'

urlpatterns = [
    path('create/', views.create_appeal, name='create_appeal'),
]