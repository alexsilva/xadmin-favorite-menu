# coding=utf-8
import json

from django.contrib.contenttypes.models import ContentType
from django.forms import Media
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.functional import cached_property
from xadmin.plugins.utils import get_context_dict
from xadmin.views import BaseAdminPlugin

from xplugin_favorite_menu.models import FavoriteMenu


class FavoriteMenuPlugin(BaseAdminPlugin):
    """
    Plugin that allows you to add favorite menus to the site menu
    """
    favorite_menu_template = "xadmin/favorite_menu/menus.html"
    favorite_menu_render_using = None  # template engine (def. django)
    favorite_menu_root_id = 'favorite-menu-box'
    favorite_menu = True

    def init_request(self, *args, **kwargs):
        return bool(self.favorite_menu)

    @cached_property
    def has_valid_context(self):
        """It only loads scripts under these conditions"""
        valid = bool(hasattr(self, 'model') and
                     not getattr(self.admin_view, 'org_obj', None))
        if valid and hasattr(self.admin_view, 'favorite_menu_permission'):
            valid &= bool(self.admin_view.favorite_menu_permission())
        return valid

    def _get_menu_queryset(self):
        """Queryset containing the existing menu"""
        if self.has_valid_context:
            return FavoriteMenu.objects.get_menu_for_model(self.model,
                                                           self.request.user,
                                                           removed=False)
        else:
            return FavoriteMenu.objects.none()

    def get_menu_options(self, menu_options):
        """related: FavoriteMenuOptionsView"""
        menu_options['target'] = self.favorite_menu_root_id
        return menu_options

    @cached_property
    def ctx_menu(self):
        """The view model menu in context"""
        return self._get_menu_queryset().first()

    @cached_property
    def has_menu(self):
        """If there is a menu assigned to the view model in the context"""
        return bool(self.ctx_menu)

    def block_top_toolbar(self, context, nodes):
        """Render the button that adds menus"""
        if not self.has_valid_context:
            return
        ajax_url = reverse("xadmin:favorite_menu_{}".format("delete" if self.has_menu else "add"))
        context = {
            'context': context,
            'has_menu': self.has_menu,
            'menu': self.ctx_menu,
            'ajax_url': ajax_url
        }
        content = render_to_string("xadmin/favorite_menu/menus_btn_top_toolbar.html",
                                   context=get_context_dict(context),
                                   using=self.favorite_menu_render_using)
        nodes.insert(0, content)

    def block_menu_nav_top(self, context, nodes):
        """Displays favorite menus"""
        queryset = FavoriteMenu.objects.filter(user=self.request.user,
                                               removed=False)
        if hasattr(self.admin_view, 'favorite_menu_filter'):
            queryset = self.admin_view.favorite_menu_filter(queryset, context)
        context = {
            'context': context,
            'menus': queryset,
            'favorite_menu_root_id': self.favorite_menu_root_id,
            'admin_site': self.admin_site
        }
        nodes.append(render_to_string(self.favorite_menu_template,
                                      using=self.favorite_menu_render_using,
                                      context=get_context_dict(context)))

    def block_extrabody(self, context, nodes):
        if not self.has_valid_context:
            return
        # Initializes the object that adds menus.
        if self.has_menu:
            data = {'id': self.ctx_menu.pk}
        else:
            ctype = ContentType.objects.get_for_model(self.model)
            data = {
                'user': self.request.user.pk,
                'content_type': ctype.pk
            }
        nodes.append(f"""
        <script type='application/javascript'>
            $(document).ready(function() {{
                var $favorite_menu = $("#btn-favorite-menu").favorite_menu({{
                    target: "#" + favorite_menu_options.target,
                    data: {json.dumps(data)}
                }});
                if ($favorite_menu) {{ $favorite_menu.bind_click() }};
            }})
        </script>
        """)

    def get_media(self, media):
        js = [reverse(f'{self.admin_site.app_name}:favorite_menu_settings')]
        if self.has_valid_context:
            # Script that does the action of adding / removing menus
            js.append('favorite_menu/js/favorite_menu.js')
        js.append('favorite_menu/js/favorite_menu_sort.js')
        media += Media(css={
            'screen': (
                'favorite_menu/css/styles.css',
            )
        }, js=js)
        return media
