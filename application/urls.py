from django.conf.urls.static import static
from django.urls import path
from application.views import RecentReleasesListView
from config import settings
from application import views

urlpatterns = [
    path('', RecentReleasesListView.as_view(), name='index'),
    path('artist_create/', views.ArtistCreateView.as_view(), name="artist_create"),
    path('album_create/', views.AlbumCreateView.as_view(), name="album_create"),
    path('<slug:slug>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('<slug:artist_slug>/<slug:album_slug>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('<slug:artist_slug>/<slug:album_slug>/<int:position>/', views.TrackDetailView.as_view(), name='track_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
