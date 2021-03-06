$(function () {
    var MenuFavorite = function ($el, options) {
        this.$el = $el;
        this.options = options;
    }

    MenuFavorite.prototype.before_send_post = function (xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", $.getCookie('csrftoken'));
    }

    MenuFavorite.prototype.post_done = function (data, text, xhr) {
        if (data.status === true) {
            location.reload(true);
        } else {
            alert(gettext("failed to create/delete menu."));
        }
    }

    MenuFavorite.prototype.post_fail = function (xhr) {
        alert(gettext("failed to create/delete menu."));
    }

    MenuFavorite.prototype.request = function () {
        var self = this;
        this.$el.addClass("disabled");
        return $.ajax({
            type: "POST",
            url: this.$el.data('ajax-url'),
            data: this.options.data || {},
            dataType: "json",
            beforeSend: this.before_send_post,
        }).done(
            $.proxy(this.post_done, this)
        ).fail(
            $.proxy(this.post_fail, this)
        ).always(function () {
            self.$el.removeClass("disabled");
        });
    }

    // get option value by name
    MenuFavorite.prototype.get_option = function (name) {
        return this.options[name];
    }

    //action bind
    MenuFavorite.prototype.bind_click = function () {
        this.$el.click($.proxy(this.request, this));
    }

    $.fn.favorite_menu = function (options) {
        if (!this.data('favorite_menu')) {
            this.data('favorite_menu', new MenuFavorite(this, options));
        }
        return this.data('favorite_menu');
    }
})
;