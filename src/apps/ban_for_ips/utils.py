from django.conf import settings
from django.core.cache import cache
from django.utils import timezone


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def reset_cache(*args, **kwargs) -> dict:
    from apps.ban_for_ips.models import BannedIp
    print('Reset banned IPs cache.')

    ips = BannedIp.objects.filter(banned_for__lte=timezone.now()).order_by('-banned_for').values('ip', 'banned_for')
    cache.set(settings.BANNED_IP_REDIS_KEY, ips)
    return ips


def get_banned_ips():
    ips = cache.get(settings.BANNED_IP_REDIS_KEY)
    if not ips:
        ips = reset_cache()
    return ips
