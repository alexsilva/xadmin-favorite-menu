# coding=utf-8
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class FavoriteMenuManager(models.Manager):

    def get_menu_for_model(self, model, user):
        return self.filter(content_type=ContentType.objects.get_for_model(model),
                           user=user)


class FavoriteMenu(models.Model):
    """Stores data about the created menus"""
    order = models.PositiveIntegerField(verbose_name=_("Order"), default=0)
    content_type = models.ForeignKey(ContentType, verbose_name=_("Content"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"))
    removed = models.BooleanField(verbose_name=_("Removed"),
                                  default=False,
                                  editable=False)
    objects = FavoriteMenuManager()

    def get_content_url(self, app_name=None):
        model_info = (self.content_type.app_label,
                      self.content_type.model)
        return reverse('xadmin:%s_%s_changelist' % model_info,
                       current_app=app_name)

    class Meta:
        verbose_name = _("Favorite Menu (plugin)")
        ordering = ('order',)

    def __str__(self):
        return f"{self.user}/{self.order}"
