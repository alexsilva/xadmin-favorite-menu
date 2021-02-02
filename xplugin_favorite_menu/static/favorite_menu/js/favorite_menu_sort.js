$(document).ready(function () {
    var menu_options = favorite_menu_options || {},
        target = "#" + menu_options.target;
    $(target).sortable({
        // html 5
        hoverClass: "cursor-move",
        forcePlaceholderSize: true,
        cursor: "move",
        // html 4
        axis: 'y',
        items: 'li',
        update: function (event, ui) {
            var $rows = $(this);
            var $item = $(ui.item);
            var data = $rows.sortable('serialize', {
                attribute: 'data-order',
                expression: (/(.+)_(\d+)/),
            });
            $item.addClass('disabled');
            $.ajax({
                url: $rows.data('post-url'),
                method: 'POST',
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $.getCookie('csrftoken'));
                },
                data: data
            }).done(function () {
                $item.removeClass('disabled'); // for safety
                //location.reload(true);
            }).fail(function () {
                $item.removeClass('disabled');
            });
        }
    }).each(function () {
        this.addEventListener('sortupdate', function (event) {
            var data = new FormData(),
                $rows = $(event.target),
                pattern = new RegExp((/(.+)_(\d+)/)),
                $item = $(event.detail.item);
            $rows.find("li").each(function () {
                var order = $(this).data("order"),
                    match = pattern.exec(order);
                if (match) data.append(match[1], match[2]);
            });
            $item.addClass('disabled');
            $.ajax({
                url: $rows.data('post-url'),
                method: 'POST',
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $.getCookie('csrftoken'));
                },
                data: data,
                contentType: false,
                processData: false,
            }).done(function () {
                $item.removeClass('disabled'); // for safety
                //location.reload(true);
            }).fail(function () {
                $item.removeClass('disabled');
            });
        });
    });
});