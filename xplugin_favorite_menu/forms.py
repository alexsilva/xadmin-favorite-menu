# coding=utf-8
from django import forms

from xplugin_favorite_menu.models import FavoriteMenu


class MenuFavoriteForm(forms.ModelForm):
    class Meta:
        model = FavoriteMenu

        exclude = (
            'order',
        )

    def save(self, commit=True):
        opts = self._meta
        try:
            instance = opts.model.objects.get(
                content_type=self.cleaned_data['content_type'],
                user=self.cleaned_data['user']
            )
            instance.removed = False
            if commit:
                instance.save()
        except opts.model.DoesNotExist:  # create a new instance
            instance = super(MenuFavoriteForm, self).save(commit=commit)
        return instance
