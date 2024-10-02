from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify
from unidecode import unidecode


class Artist(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    artist_cover = models.ImageField(upload_to='artist_pics/', default='artist_pics/default_cover.jpg')

    def get_absolute_url(self):
        return reverse_lazy('artist_detail', args=[self.slug])


class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    album_cover = models.ImageField(upload_to='album_covers/', default='album_covers/default_cover.jpg')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('album_detail', args=[self.artist.slug, self.slug])

    class Meta:
        unique_together = ('artist', 'title',)


class Track(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    lyrics = models.TextField()
    position = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        if not self.id:
            existing_tracks = Track.objects.filter(album=self.album)
            if existing_tracks.exists():
                self.position = existing_tracks.order_by('-position').first().position + 1
            else:
                self.position = 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('track_detail', args=[self.album.artist.slug, self.album.slug, self.position])
