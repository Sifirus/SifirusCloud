from users.models import Profile

def avatar_context_processor(request):
    avatar = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            avatar = profile.avatar
        except Profile.DoesNotExist:
            # Если профиль не создан, можно оставить avatar = None
            pass
    return {'avatar': avatar}