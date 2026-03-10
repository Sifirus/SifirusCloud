from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .forms import TrackForm
from tracks.models import Track


def index(request):
    if request.user.is_authenticated:
        tracks = Track.objects.order_by('-created_at')
        return render(request, 'tracks/index.html', {'tracks': tracks})
    else:
        return render(request, 'users/guest.html')


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


class TrackUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Track
    form_class = TrackForm
    template_name = 'tracks/track_form.html'
    success_url = reverse_lazy('tracks:index')

    def test_func(self):
        track = self.get_object()
        return self.request.user == track.uploaded_by

class TrackDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Track
    template_name = 'tracks/track_confirm_delete.html'
    success_url = reverse_lazy('tracks:index')

    def test_func(self):
        track = self.get_object()
        return self.request.user == track.uploaded_by