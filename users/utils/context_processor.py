from users.models import Profile


def avatar_context_processor(request):
    context = {'avatar': None}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        avatar = profile.avatar
        context['avatar'] = avatar
    return context