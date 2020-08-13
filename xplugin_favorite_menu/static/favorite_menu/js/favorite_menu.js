$(function () {
    $.fn.favorite_menu = function (options) {
        var MenuFavorite = function ($this, options) {
            this.$this = $this;
            this.options = options;
        }

        MenuFavorite.prototype.before_send_post = function (xhr, settings) {
            var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
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
            this.$this.addClass("disabled");
            return $.ajax({
                type: "POST",
                url: this.$this.data('ajax-url'),
                data: this.options.data || {},
                dataType: "json",
                beforeSend: this.before_send_post,
            }).done(
                $.proxy(this.post_done, this)
            ).fail(
                $.proxy(this.post_fail, this)
            ).always(function() {
                self.$this.removeClass("disabled");
            });
        }

        //action bind
        MenuFavorite.prototype.bind_click = function () {
            this.$this.click($.proxy(this.request, this));
        }

        if (!this.data('favorite_menu')) {
            this.data('favorite_menu', new MenuFavorite(this, options));
        }
        return this.data('favorite_menu');
    }
})
;