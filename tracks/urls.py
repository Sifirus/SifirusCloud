from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'tracks'  # обязательно для пространства имён

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.TrackCreateView.as_view(), name='track_upload'),
    path('<int:pk>/edit/', views.TrackUpdateView.as_view(), name='track_edit'),
    path('<int:pk>/delete/', views.TrackDeleteView.as_view(), name='track_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)