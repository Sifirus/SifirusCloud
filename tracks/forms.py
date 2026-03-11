from django import forms
from .models import Track

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title','artist', 'description', 'genre', 'audio_file', 'cover_image']