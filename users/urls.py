from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name='register'),
    path('author/<int:user_id>', views.render_profile, name='profile'),
    path('author/<int:user_id>/edit', views.edit_profile, name='edit_profile'),

]