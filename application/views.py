from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView
from unidecode import unidecode

from application.forms import ArtistCreateForm, AlbumCreateForm
from application.models import Artist, Album, Track


class AlbumCreateView(LoginRequiredMixin, CreateView):
    form_class = AlbumCreateForm
    template_name = 'application/album_create.html'
    success_url = reverse_lazy('index')


class ArtistCreateView(LoginRequiredMixin, CreateView):
    form_class = ArtistCreateForm
    template_name = 'application/artist_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        name = form.cleaned_data['name']
        slug = slugify(unidecode(name))
        if Artist.objects.filter(slug=slug).exists():
            form.add_error('name', 'Artist with this name already exists')
            return self.form_invalid(form)
        form.instance.slug = slug
        return super().form_valid(form)


class RecentReleasesListView(ListView):
    model = Album
    context_object_name = 'albums'
    template_name = 'application/recent_releases.html'

    def get_queryset(self):
        return Album.objects.order_by('-release_date')[:5]


class ArtistDetailView(DetailView):
    model = Artist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        albums = Album.objects.filter(artist=self.get_object())
        context['albums'] = albums
        return context


class AlbumDetailView(DetailView):
    model = Album

    def get_object(self, queryset=None):
        artist_slug = self.kwargs.get('artist_slug')
        album_slug = self.kwargs.get('album_slug')
        return get_object_or_404(Album, slug=album_slug, artist__slug=artist_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tracks = Track.objects.filter(album=self.get_object())
        context['tracks'] = tracks
        return context


class TrackDetailView(DetailView):
    model = Track

    def get_object(self, queryset=None):
        artist_slug = self.kwargs.get('artist_slug')
        album_slug = self.kwargs.get('album_slug')
        position = self.kwargs.get('position')

        album = get_object_or_404(Album, slug=album_slug, artist__slug=artist_slug)
        track = get_object_or_404(Track, album=album, position=position)
        return track
