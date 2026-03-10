from users.models import Profile


def avatar_context_processor(request):
    profile = Profile.objects.get(user=request.user)
    avatar = profile.avatar
    return {'avatar': avatar}