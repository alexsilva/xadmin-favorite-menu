from django import template
from django.apps import apps as django_apps

register = template.Library()


def _get_opts(model):
    return model._meta

@register.filter
def opts(model, name):
    return getattr(_get_opts(model), name)

@register.filter
def apps(model, name):
    app_config = django_apps.get_app_config(
        _get_opts(model).app_label
    )
    return getattr(app_config, name)
