# coding=utf-8
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.urls import reverse
from xadmin.plugins.utils import get_context_dict
from xadmin.views import BaseAdminPlugin

from xplugin_menu_favorite.models import MenuFavorite


class MenuFavoritePlugin(BaseAdminPlugin):
    """
    Plugin that allows you to add favorite menus to the site menu
    """
    menu_favorite_template = "xadmin/menu_favorite/menus.html"
    menu_favorite_render_using = None  # template engine (def. django)
    menu_favorite = True

    def init_request(self, *args, **kwargs):
        return bool(self.menu_favorite)

    def block_top_toolbar(self, context, nodes):
        """Render the button that adds menus"""
        model = self.admin_view.model
        queryset = MenuFavorite.objects.get_menu_for_model(model, self.request.user)
        context = {
            'context': context,
            'has_menu': queryset.exists(),
            'queryset': queryset
        }
        content = render_to_string("xadmin/menu_favorite/menus_btn_top_toolbar.html",
                                   context=get_context_dict(context),
                                   using=self.menu_favorite_render_using)
        nodes.insert(0, content)

    def block_extra_slide_menu(self, context, nodes):
        """"""
        context = {
            'context': context,
            'menus': MenuFavorite.objects.all()
        }
        nodes.append(render_to_string(self.menu_favorite_template,
                                      using=self.menu_favorite_render_using,
                                      context=get_context_dict(context)))

    def block_extrabody(self, context, nodes):
        # Initializes the object that adds menus.
        ctype = ContentType.objects.get_for_model(self.model)
        url = reverse("xadmin:menu_favorite_add")
        nodes.append(f"""
        <script>
            $(document).ready(function() {{
                $("#btn-menu-favorite").menu_favorite({{
                    url: "{url}",
                    data: {{ 
                        user: {self.request.user.pk},
                        content_type: {ctype.pk}
                    }}
                }}).bind_click();
            }})
        </script>
        """)

    def get_media(self, media):
        media.add_js((
            # Script that does the action of adding / removing menus
            'menu_favorite/js/menu_favorite.js',
        ))
        return media
