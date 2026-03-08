from django.http import HttpResponseRedirect
from django.shortcuts import render

def index(request):
    if request.user.is_authenticated:
        return render(request, 'tracks/index.html')
    else:
        return render(request, 'users/guest.html')