# coding=utf-8
import json

from django.http import JsonResponse, HttpResponse
from django.utils.functional import cached_property
from django.views.generic import FormView
from xadmin.views import BaseAdminView, filter_hook

from xplugin_favorite_menu.forms import MenuFavoriteForm
from xplugin_favorite_menu.models import FavoriteMenu


class FavoriteMenuOptionsView(BaseAdminView):

    def get(self, request, **kwargs):
        menu_options = json.dumps(self.get_menu_options())
        script_js = f"""var favorite_menu_options={menu_options}"""
        return HttpResponse(script_js, content_type='application/javascript')

    @filter_hook
    def get_menu_options(self):
        return {}


class FavoriteMenuCreateView(BaseAdminView, FormView):
    """Create / Remove Menus Favorite"""
    http_method_names = ['post']
    form_class = MenuFavoriteForm

    @filter_hook
    def form_valid(self, form):
        instance = form.save()
        return JsonResponse({
            'status': True,
            'create': True
        })

    def form_invalid(self, form):
        return JsonResponse({
            'form': form.errors
        })


class FavoriteMenuDeleteView(BaseAdminView):
    http_method_names = ['post']
    model = FavoriteMenu

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opts = self.model._meta

    @cached_property
    def object_id(self):
        return int(self.request.POST['id'])

    def get_object(self):
        return self.model.objects.get(pk=self.object_id)

    @filter_hook
    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        if not self.object.removed:
            self.object.removed = True
            self.object.save()
        return JsonResponse({
            'status': True,
            'delete': True
        })

    # Add support for browsers which only accept GET and POST for now.
    def post(self, request, *args, **kwargs):
        try:
            response = self.delete(request, *args, **kwargs)
        except ValueError:
            response = JsonResponse({
                'error': "'id' is a required option"
            })
        return response


class FavoriteMenuOrderView(BaseAdminView):
    """Reorder the menus"""
    http_method_names = ['post']
    model = FavoriteMenu

    @staticmethod
    def get_list(request, name):
        options = request.POST
        return (options.getlist(name) or
                options.getlist(f'{name}[]'))

    def post(self, request, **kwargs):
        order_objs = self.get_list(request, 'order')
        for order_value, pk in enumerate(order_objs, start=1):
            instance = self.model.objects.get(pk=pk)
            old_order = instance.order
            instance.order = order_value
            if old_order != order_value:
                instance.save()
        return JsonResponse({
            'status': True
        })
