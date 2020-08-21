$(document).ready(function () {
    var menu_options = favorite_menu_options || {};
    $("#" + menu_options.target).sortable({
        cursor: "move",
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