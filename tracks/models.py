from django.db import models
from django.contrib.auth.models import User


class Track(models.Model):
    GENRE_CHOICES = [
        ('electronic', 'Электроника'),
        ('pop', 'Поп'),
        ('rock', 'Рок'),
        ('hiphop', 'Хип-хоп'),
        ('jazz', 'Джаз'),
        ('rnb', 'R&B'),
        ('classical', 'Классика'),
        ('lofi', 'Lo-fi'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название")
    artist = models.CharField(max_length=200, verbose_name="Исполнитель")
    description = models.TextField(verbose_name="Описание", blank=True)
    audio_file = models.FileField(upload_to='tracks/', verbose_name="Аудиофайл")
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name="Обложка")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracks', verbose_name="Загрузил")
    plays_count = models.IntegerField(default=0, verbose_name="Прослушивания")
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, verbose_name="Жанр", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Трек"
        verbose_name_plural = "Треки"

    def __str__(self):
        return f"{self.uploaded_by} - {self.title}"

    def likes_count(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track')
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def __str__(self):
        return f"{self.user.username} → {self.track.title}"


class Playlist(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Публичный'),
        ('link', 'Только по ссылке'),
        ('private', 'Приватный'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    cover_image = models.ImageField(upload_to='playlist_covers/', blank=True, null=True, verbose_name="Обложка")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists', verbose_name="Владелец")
    tracks = models.ManyToManyField(Track, blank=True, related_name='playlists', verbose_name="Треки")
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='private', verbose_name="Видимость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Плейлист"
        verbose_name_plural = "Плейлисты"

    def __str__(self):
        return f"{self.owner.username} - {self.name}"
