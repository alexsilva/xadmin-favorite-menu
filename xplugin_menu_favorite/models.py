# coding=utf-8
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class MenuFavorite(models.Model):
    """Stores data about the created menus"""
    order = models.PositiveIntegerField(verbose_name=_("Order"))
    content_type = models.ForeignKey(ContentType, verbose_name=_("Content"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"))

    class Meta:
        verbose_name = _("Favorite Menu (plugin)")
        ordering = ('order',)

    def __str__(self):
        return f"{self.user}/{self.order}"
