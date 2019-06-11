var csrftoken = getCookie('csrftoken');
$(document).ready(function () {

    $(".message-recipients").popover({
        placement: 'right',
        title: '',
        html: 'true',
        content: function () {
            var tag_div = $(this).next();
            return tag_div.html();
        }
    });

    $(document).on('click', '.popover-close', function () {
        $(".evaluation-rotation").popover('hide');
    });

    // Delete inbox for js
    $(document).on('click', 'a.delete-inbox-msg', function(){
        var link = $(this);
        $.confirm({
          'text': '<b>Are you sure?</b>',
          confirm: function () {
              $.ajax({
                type: "POST",
                url: URLS.user_inbox_delete_message.replace('44444444', link.data("id")),
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (res) {
                    link.parents("tr").remove();
                    var message_dialog = $("#message-dialog");
                    message_dialog.find('p strong').html('Successfully deleted');
                    message_dialog.alert().show();
                    $(window).scrollTop($('#message-dialog').offset().top);
                    message_dialog.fadeOut(10000);
                }
              });
          },
          cancel: function (button) {
          },
          confirmButton: "Yes",
          cancelButton: "Cancel"
        });
    });

    // Delete message from outbox js
    $(document).on('click', 'a.delete-outbox-msg', function(){
        var link = $(this);
        $.confirm({
          'text': '<b>Are you sure?</b>',
          confirm: function () {
              $.ajax({
                type: "POST",
                url: URLS.user_outbox_delete_message.replace('44444444', link.data("id")),
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (res) {
                    link.parents("tr").remove();
                    var message_dialog = $("#message-dialog");
                    message_dialog.find('p strong').html('Successfully deleted');
                    message_dialog.alert().show();
                    $(window).scrollTop($('#message-dialog').offset().top);
                    message_dialog.fadeOut(10000);
                }
              });
          },
          cancel: function (button) {
          },
          confirmButton: "Yes",
          cancelButton: "Cancel"
        });
    });
});

