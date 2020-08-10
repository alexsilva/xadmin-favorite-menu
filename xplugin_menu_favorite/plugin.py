from django.template.loader import render_to_string
from xadmin.views import BaseAdminPlugin

from xplugin_menu_favorite.models import MenuFavorite


class MenuFavoritePlugin(BaseAdminPlugin):
    """
    Plugin that allows you to add favorite menus to the menu menu
    """
    menu_favorite_template = "xadmin/menu_favorite/menus.html"
    menu_favorite_template_using = None  # template engine (def. django)
    menu_favorite = True

    def init_request(self, *args, **kwargs):
        return bool(self.menu_favorite)

    def block_extra_slide_menu(self, context, nodes):
        """"""
        context = {
            'context': context,
            'menus': MenuFavorite.objects.all()
        }
        nodes.append(render_to_string(self.menu_favorite_template,
                                      using=self.menu_favorite_template_using,
                                      context=context))
