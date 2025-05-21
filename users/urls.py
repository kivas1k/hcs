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
    path('admin/tags/', views.tag_admin, name='tag_admin'),
    path('admin/tags/create/', views.create_tag, name='create_tag'),
    path('admin/tags/<int:pk>/edit/', views.edit_tag, name='edit_tag'),
    path('admin/tags/<int:pk>/delete/', views.delete_tag, name='delete_tag'),
    path('admin/status/<str:model_type>/', views.status_admin, name='status_admin'),
    path('admin/status/<str:model_type>/create/', views.create_status, name='create_status'),
    path('admin/status/<str:model_type>/<int:pk>/edit/', views.edit_status, name='edit_status'),
    path('admin/status/<str:model_type>/<int:pk>/delete/', views.delete_status, name='delete_status'),
]