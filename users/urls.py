from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('admin/', views.admin_panel, name='admin_panel'),
    path('admin/users/', views.user_admin, name='user_admin'),
    path('admin/users/<int:pk>/edit/', views.edit_user_role, name='edit_user_role'),
]