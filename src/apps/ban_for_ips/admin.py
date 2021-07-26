from django.contrib import admin

# Register your models here.
from apps.ban_for_ips.models import BannedIp


@admin.register(BannedIp)
class BannedIpAdmin(admin.ModelAdmin):
    search_fields = ('ip', )
