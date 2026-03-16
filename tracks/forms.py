from django import forms
from .models import Track, Playlist


class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'artist', 'description', 'genre', 'audio_file', 'cover_image']


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'description', 'cover_image', 'visibility']
