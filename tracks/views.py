from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Track
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Track
from .forms import TrackForm

def index(request):
    # Получаем все треки из базы, можно отсортировать по дате
    tracks = Track.objects.all().order_by('-created_at')
    
    if request.user.is_authenticated:
        return render(request, 'tracks/index.html', {'tracks': tracks})
    else:
        return render(request, 'users/guest.html', {'tracks': tracks})  # если хотим показывать треки гостям
class TrackCreateView(LoginRequiredMixin, CreateView):
    model = Track
    form_class = TrackForm
    template_name = 'tracks/track_form.html'
    success_url = reverse_lazy('tracks:index')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)


class TrackUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Track
    form_class = TrackForm
    template_name = 'tracks/track_form.html'
    success_url = reverse_lazy('tracks:index')

    def test_func(self):
        track = self.get_object()
        return self.request.user == track.uploaded_by or self.request.user.is_superuser


class TrackDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Track
    template_name = 'tracks/track_confirm_delete.html'
    success_url = reverse_lazy('tracks:index')

    def test_func(self):
        track = self.get_object()
        return self.request.user == track.uploaded_by or self.request.user.is_superuser