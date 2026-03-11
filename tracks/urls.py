from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


app_name = 'tracks'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.TrackCreateView.as_view(), name='track_upload'),
    path('track/<int:pk>', views.TrackDetailView.as_view(), name='track_detail'),
    path('track/<int:pk>/update/', views.TrackUpdateView.as_view(), name='track_update'),
    path('track/<int:pk>/edit/', views.TrackUpdateView.as_view(), name='track_edit'),
    path('track/<int:pk>/delete/', views.TrackDeleteView.as_view(), name='track_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)