# coding=utf-8
from django import forms

from xplugin_favorite_menu.models import MenuFavorite


class MenuFavoriteForm(forms.ModelForm):
    class Meta:
        model = MenuFavorite

        exclude = (
            'order',
        )
