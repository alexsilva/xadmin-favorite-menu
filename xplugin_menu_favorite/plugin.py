from xadmin.views import BaseAdminPlugin


class MenuFavoritePlugin(BaseAdminPlugin):
    """Plugin that allows you to add favorite menus to the menu menu"""
    menu_favorite = True

    def init_request(self, *args, **kwargs):
        return bool(self.menu_favorite)

    def block_extra_slide_menu(self, context, nodes):
        """"""

        # nodes.append
