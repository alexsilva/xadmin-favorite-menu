# coding=utf-8
from django.http import JsonResponse
from django.views.generic import FormView
from xadmin.views import BaseAdminView, filter_hook

from xplugin_menu_favorite.forms import MenuFavoriteForm


class MenuFavoriteView(BaseAdminView, FormView):
    """Create / Remove Menus Favorite"""
    http_method_names = ['post']
    form_class = MenuFavoriteForm

    @filter_hook
    def form_valid(self, form):
        instance = form.save()
        return instance

    def form_invalid(self, form):
        return JsonResponse({
            'form': form.errors
        })
