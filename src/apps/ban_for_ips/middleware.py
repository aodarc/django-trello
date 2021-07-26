from django.http.response import HttpResponseForbidden
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from apps.ban_for_ips.utils import get_banned_ips, get_client_ip


class IPBanMiddleware(MiddlewareMixin):
    def process_request(self, request):
        client_id = get_client_ip(request)

        check_ban = next((row for row in get_banned_ips()
                          if client_id == row['ip'] and timezone.now() > row['banned_for']
                          ), None)
        if check_ban:
            return HttpResponseForbidden()
