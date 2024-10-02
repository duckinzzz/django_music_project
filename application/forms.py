from django import forms
from application.models import Artist, Album


class ArtistCreateForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name']


class AlbumCreateForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['artist', 'title', 'genre', 'release_date', 'album_cover']
