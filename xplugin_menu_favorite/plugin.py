# coding=utf-8
import json

from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.functional import cached_property
from xadmin.plugins.utils import get_context_dict
from xadmin.views import BaseAdminPlugin

from xplugin_menu_favorite.models import MenuFavorite


class MenuFavoritePlugin(BaseAdminPlugin):
    """
    Plugin that allows you to add favorite menus to the site menu
    """
    menu_favorite_template = "xadmin/menu_favorite/menus.html"
    menu_favorite_render_using = None  # template engine (def. django)
    menu_favorite_root_id = 'menu-favorite-box'
    menu_favorite = True

    def init_request(self, *args, **kwargs):
        return bool(self.menu_favorite and
                    getattr(self.admin_view, 'model', None))

    def _get_menu_queryset(self):
        """Queryset containing the existing menu"""
        return MenuFavorite.objects.get_menu_for_model(self.model,
                                                       self.request.user)

    @cached_property
    def menu_queryset(self):
        return self._get_menu_queryset()

    def block_top_toolbar(self, context, nodes):
        """Render the button that adds menus"""
        has_menu = self.menu_queryset.exists()
        ajax_url = reverse("xadmin:menu_favorite_{}".format("delete" if has_menu else "add"))
        context = {
            'context': context,
            'has_menu': has_menu,
            'queryset': self.menu_queryset,
            'ajax_url': ajax_url
        }
        content = render_to_string("xadmin/menu_favorite/menus_btn_top_toolbar.html",
                                   context=get_context_dict(context),
                                   using=self.menu_favorite_render_using)
        nodes.insert(0, content)

    def block_menu_nav(self, context, nodes):
        """Displays favorite menus"""
        context = {
            'context': context,
            'menus': MenuFavorite.objects.all(),
            'menu_favorite_root_id': self.menu_favorite_root_id,
            'admin_site': self.admin_site
        }
        nodes.append(render_to_string(self.menu_favorite_template,
                                      using=self.menu_favorite_render_using,
                                      context=get_context_dict(context)))

    def block_extrabody(self, context, nodes):
        # Initializes the object that adds menus.
        has_menu = self.menu_queryset.exists()
        if has_menu:
            data = {'id': self.menu_queryset.first().pk}
        else:
            ctype = ContentType.objects.get_for_model(self.model)
            data = {
                'user': self.request.user.pk,
                'content_type': ctype.pk
            }
        data = json.dumps(data)
        nodes.append(f"""
        <script>
            $(document).ready(function() {{
                $("#btn-menu-favorite").menu_favorite({{
                    target: "#{self.menu_favorite_root_id}",
                    data: {data}
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
