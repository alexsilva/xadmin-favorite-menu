# coding=utf-8
import xadmin.sites
from xadmin.views import CommAdminView


def register(site=None):
    """Register the plugin in the ListAdminView class"""
    if site is None:
        site = xadmin.sites.site

    from xplugin_favorite_menu.plugin import MenuFavoritePlugin
    from xplugin_favorite_menu.views import FavoriteMenuCreateView, FavoriteMenuDeleteView, FavoriteMenuOrderView

    site.register_plugin(MenuFavoritePlugin, CommAdminView)
    site.register_plugin(MenuFavoritePlugin, FavoriteMenuCreateView)
    site.register_plugin(MenuFavoritePlugin, FavoriteMenuDeleteView)

    site.register_view('favorite-menu/add', FavoriteMenuCreateView, "favorite_menu_add")
    site.register_view('favorite-menu/delete', FavoriteMenuDeleteView, "favorite_menu_delete")
    site.register_view(r'favorite-menu/order/', FavoriteMenuOrderView, "favorite_menu_order")