from django.db import models


class TaskManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('comments').all()
