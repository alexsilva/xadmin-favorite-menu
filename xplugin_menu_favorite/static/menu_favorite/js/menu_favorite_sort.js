$(function () {
    var menu = $("#btn-menu-favorite").data('menu_favorite');
    $(menu.options.target).sortable({
        cursor: "move",
        change: function (event, ui) {
            $(ui.item).attr("data-order", "order_" + ui.item.index());
        },
        update: function (event, ui) {
            var $rows = $(this);
            var $item = ui.item;
            var data = $rows.sortable('serialize', {
                attribute: 'data-order',
                expression: (/(.+)_(\d+)/),
            });
            console.log(data)
            $item.addClass('disabled');
            $.ajax({
                url: $rows.data('post-url'),
                method: 'POST',
                beforeSend: function(xhr, settings) {
                    var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                data: data
            }).done(function () {
                $item.removeClass('disabled'); // for safety
                //location.reload(true);
            }).fail(function () {
                $item.removeClass('disabled');
            });
        }
    });
});