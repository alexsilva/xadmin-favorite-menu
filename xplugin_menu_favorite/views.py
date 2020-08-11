# coding=utf-8
from django.http import JsonResponse
from django.views.generic import FormView
from xadmin.views import BaseAdminView

from xplugin_menu_favorite.forms import MenuFavoriteForm


class MenuFavoriteView(BaseAdminView, FormView):
    """"""
    form_class = MenuFavoriteForm
    template_name = ''

    def form_valid(self, form):
        return JsonResponse({
            'status': True
        })

    def form_invalid(self, form):
        return JsonResponse({
            'form': form.errors
        })
