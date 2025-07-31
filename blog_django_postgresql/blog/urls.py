from django.urls import path
from . import views

urlpatterns = [
    # Authentication Endpoints
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_update, name='profile_update'),
    path('logout/', views.logout_view, name='logout'),
    
    # Blog Post Endpoints
    path('post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/comments/', views.add_comment, name='add_comment'),

    # CSRF Token Endpoint
    path('csrf/', views.get_csrf_token, name='get_csrf_token'),
]
