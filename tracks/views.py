from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.db.models import Sum, Count
from django.views.decorators.http import require_POST
from .forms import TrackForm, PlaylistForm
from tracks.models import Track, Playlist, Like


def index(request):
    if request.user.is_authenticated:
        newest_tracks = Track.objects.order_by('-created_at')[:8]
        return render(request, 'tracks/index.html', {'newest_tracks': newest_tracks})
    else:
        return render(request, 'users/guest.html')


@login_required(login_url='login')
def library(request):
    # Реальные лайкнутые треки
    liked_track_ids = Like.objects.filter(user=request.user).values_list('track_id', flat=True)
    liked_tracks = Track.objects.filter(pk__in=liked_track_ids).order_by('-likes__created_at')
    my_tracks_count = Track.objects.filter(uploaded_by=request.user).count()
    playlists = Playlist.objects.filter(owner=request.user).order_by('-created_at')

    return render(request, 'tracks/library.html', {
        'liked_tracks': liked_tracks,
        'my_tracks_count': my_tracks_count,
        'playlists': playlists,
    })


class TrackCreateView(LoginRequiredMixin, CreateView):
    model = Track
    form_class = TrackForm
    template_name = 'tracks/track_form.html'
    success_url = reverse_lazy('tracks:index')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)


class TrackDetailView(LoginRequiredMixin, DetailView):
    model = Track
    template_name = 'tracks/track_detail.html'
    context_object_name = 'track'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            ctx['is_liked'] = Like.objects.filter(user=self.request.user, track=self.object).exists()
        ctx['likes_count'] = self.object.likes_count()
        return ctx


class TrackUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Track
    form_class = TrackForm
    template_name = 'tracks/track_form.html'
    success_url = reverse_lazy('tracks:index')

    def test_func(self):
        return self.request.user == self.get_object().uploaded_by


class TrackDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Track
    template_name = 'tracks/track_confirm_delete.html'
    success_url = reverse_lazy('tracks:index')

    def test_func(self):
        return self.request.user == self.get_object().uploaded_by


# Лайки и прослушивания

@login_required(login_url='login')
@require_POST
def toggle_like(request, pk):
    """Лайк/анлайк трека (AJAX)."""
    track = get_object_or_404(Track, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, track=track)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': track.likes_count()})


@require_POST
def track_play(request, pk):
    """Увеличить счётчик прослушиваний (AJAX)."""
    track = get_object_or_404(Track, pk=pk)
    track.plays_count += 1
    track.save(update_fields=['plays_count'])
    return JsonResponse({'plays': track.plays_count})


# Статистика

@login_required(login_url='login')
def stats(request):
    """Страница статистики пользователя."""
    user_tracks = Track.objects.filter(uploaded_by=request.user)
    total_plays = user_tracks.aggregate(s=Sum('plays_count'))['s'] or 0
    total_likes = Like.objects.filter(track__uploaded_by=request.user).count()
    top_tracks = user_tracks.order_by('-plays_count')[:5]

    # Лайки по топ трекам
    top_likes = []
    for t in top_tracks:
        top_likes.append({'track': t, 'likes': t.likes_count()})

    return render(request, 'tracks/stats.html', {
        'total_plays': total_plays,
        'total_likes': total_likes,
        'tracks_count': user_tracks.count(),
        'top_tracks': top_tracks,
        'top_likes': top_likes,
    })


# Плейлисты

@login_required(login_url='login')
def playlist_create(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.owner = request.user
            playlist.save()
            return redirect('tracks:playlist_detail', pk=playlist.pk)
    else:
        form = PlaylistForm()
    return render(request, 'tracks/playlist_form.html', {'form': form})


@login_required(login_url='login')
def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    tracks = playlist.tracks.all()
    available_tracks = Track.objects.exclude(
        pk__in=tracks.values_list('pk', flat=True)
    ).order_by('-created_at')[:20]
    return render(request, 'tracks/playlist_detail.html', {
        'playlist': playlist,
        'tracks': tracks,
        'available_tracks': available_tracks,
    })


@login_required(login_url='login')
def playlist_add_track(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, owner=request.user)
    track_id = request.POST.get('track_id')
    if track_id:
        playlist.tracks.add(get_object_or_404(Track, pk=track_id))
    return redirect('tracks:playlist_detail', pk=pk)


@login_required(login_url='login')
def playlist_remove_track(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, owner=request.user)
    track_id = request.POST.get('track_id')
    if track_id:
        playlist.tracks.remove(get_object_or_404(Track, pk=track_id))
    return redirect('tracks:playlist_detail', pk=pk)
