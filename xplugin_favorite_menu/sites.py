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

    site.register_view('favorite-menu/add', MenuFavoriteCreateView, "favorite_menu_add")
    site.register_view('favorite-menu/delete', MenuFavoriteDeleteView, "favorite_menu_delete")
    site.register_view(r'favorite-menu/order/', MenuFavoriteOrderView, "favorite_menu_order")