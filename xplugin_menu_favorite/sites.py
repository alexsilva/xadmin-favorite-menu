# coding=utf-8
import xadmin.sites
from xadmin.views import CommAdminView


def register(site=None):
    """Register the plugin in the ListAdminView class"""
    if site is None:
        site = xadmin.sites.site

    from xplugin_menu_favorite.plugin import MenuFavoritePlugin
    from xplugin_menu_favorite.views import MenuFavoriteView

    site.register_plugin(MenuFavoritePlugin, CommAdminView)
    site.register_plugin(MenuFavoritePlugin, MenuFavoriteView)

    site.register_view('menu-favorite/add', MenuFavoriteView, "menu_favorite_add")