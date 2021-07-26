from django.db import models

# Create your models here.
from django.db.models.signals import post_delete, post_save

from apps.ban_for_ips.utils import reset_cache
from common.models import BaseDateAuditModel


class BannedIp(BaseDateAuditModel):
    ip = models.GenericIPAddressField()
    banned_for = models.DateTimeField()

    def __str__(self):
        return self.ip


post_save.connect(receiver=reset_cache, sender=BannedIp)
post_delete.connect(receiver=reset_cache, sender=BannedIp)
