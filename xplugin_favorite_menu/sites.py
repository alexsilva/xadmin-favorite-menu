# coding=utf-8
import xadmin.sites
from xadmin.views import CommAdminView


def register(site=None):
    """Register the plugin in the ListAdminView class"""
    if site is None:
        site = xadmin.sites.site

    from xplugin_favorite_menu.plugin import MenuFavoritePlugin
    from xplugin_favorite_menu.views import MenuFavoriteCreateView, MenuFavoriteDeleteView, MenuFavoriteOrderView

    site.register_plugin(MenuFavoritePlugin, CommAdminView)
    site.register_plugin(MenuFavoritePlugin, MenuFavoriteCreateView)
    site.register_plugin(MenuFavoritePlugin, MenuFavoriteDeleteView)

    site.register_view('menu-favorite/add', MenuFavoriteCreateView, "menu_favorite_add")
    site.register_view('menu-favorite/delete', MenuFavoriteDeleteView, "menu_favorite_delete")
    site.register_view(r'menu-favorite/order/', MenuFavoriteOrderView, "menu_favorite_order")