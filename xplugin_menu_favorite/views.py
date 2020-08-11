# coding=utf-8
from django.http import JsonResponse
from django.utils.functional import cached_property
from django.views.generic import FormView
from xadmin.views import BaseAdminView, filter_hook

from xplugin_menu_favorite.forms import MenuFavoriteForm
from xplugin_menu_favorite.models import MenuFavorite


class MenuFavoriteCreateView(BaseAdminView, FormView):
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


class MenuFavoriteDeleteView(BaseAdminView):
    http_method_names = ['post']
    model = MenuFavorite

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
        self.object.delete()
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


class MenuFavoriteOrderView(BaseAdminView):
    """Reorder the menus"""
    http_method_names = ['post']
    model = MenuFavorite

    def post(self, request, **kwargs):
        orders = request.POST.getlist('order[]')
        for index, instance in enumerate(self.model.objects.all()):
            instance.order = int(orders[index])
            instance.save()
        return JsonResponse({
            'status': True
        })
