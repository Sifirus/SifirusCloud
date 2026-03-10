from random import choices

from django.db import models
from django.contrib.auth.models import User


class Track(models.Model):
    GENRE_CHOISES = [('фигня', 'хрень')]

    title = models.CharField(max_length=200, verbose_name="Название")
    artist = models.CharField(max_length=200, verbose_name="Исполнитель", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    audio_file = models.FileField(upload_to='media/tracks/', verbose_name="Аудиофайл")
    cover_image = models.ImageField(upload_to='media/covers/', blank=True, null=True, verbose_name="Обложка")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracks', verbose_name="Загрузил")
    plays_count = models.IntegerField(default=0, verbose_name="Прослушивания")
    genre = models.CharField(max_length=100, choices=GENRE_CHOISES, verbose_name="Жанр", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Трек"
        verbose_name_plural = "Треки"

    def __str__(self):
        return "{self.uploaded_by} - {self.title}"