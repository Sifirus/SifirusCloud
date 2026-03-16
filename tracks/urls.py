from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'tracks'

urlpatterns = [
    path('', views.index, name='index'),
    path('library/', views.library, name='library'),
    path('stats/', views.stats, name='stats'),
    path('upload/', views.TrackCreateView.as_view(), name='track_upload'),
    path('track/<int:pk>', views.TrackDetailView.as_view(), name='track_detail'),
    path('track/<int:pk>/update/', views.TrackUpdateView.as_view(), name='track_update'),
    path('track/<int:pk>/edit/', views.TrackUpdateView.as_view(), name='track_edit'),
    path('track/<int:pk>/delete/', views.TrackDeleteView.as_view(), name='track_delete'),
    path('track/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('track/<int:pk>/play/', views.track_play, name='track_play'),

    # Плейлисты
    path('playlist/create/', views.playlist_create, name='playlist_create'),
    path('playlist/<int:pk>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:pk>/add/', views.playlist_add_track, name='playlist_add_track'),
    path('playlist/<int:pk>/remove/', views.playlist_remove_track, name='playlist_remove_track'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
