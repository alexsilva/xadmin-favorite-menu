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


@register.simple_tag
def sites(instance, site):
    return instance.get_content_url(site)


@register.simple_tag
def has_admin_site_registry(admin_site, model_class):
    """Checks if the model is registered on the admin site"""
    return bool(admin_site.get_registry(model_class, None))


@register.simple_tag(takes_context=True)
def get_admin_model_icon(context, model_class, default=None):
    """Checks if the model is registered on the admin site"""
    return context['admin_view'].get_model_icon(model_class) or default
