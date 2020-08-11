# coding=utf-8
from django import forms

from xplugin_favorite_menu.models import FavoriteMenu


class MenuFavoriteForm(forms.ModelForm):
    class Meta:
        model = FavoriteMenu

        exclude = (
            'order',
        )
