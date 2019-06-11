var csrftoken = getCookie('csrftoken');
var is_room_avaliable = parseInt(room_avaliable);
$(document).on('change', '#id-room-list', function(){
    var room_id = $(this).val();
    var new_automation_url = "/dashboard/rooms/automation/create/"+room_id;
    $("#id-add-event").attr("href", new_automation_url);
    $.ajax({
        type: 'POST',
        url: URLS.dashboard_room_automations.replace("11111111", room_id),
        success: function(response){
            $("#automation-table tbody").html(response.automation_data);
        }
    })
});

// Delete automation for js
$(document).on('click', 'a.automation_delete_btn', function(){
    var link = $(this);
    $.confirm({
      'text': '<b>Are you sure?</b>',
      confirm: function () {
          $.ajax({
            type: "POST",
            url: URLS.automation_delete.replace('11111111', link.data("automation-id")),
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

$("#id-add-event").click(function(){
  if(!is_room_avaliable){
    $("#eventCreateWarningMsg").modal({
      backdrop: 'static'
    });
    return false;
  }
});