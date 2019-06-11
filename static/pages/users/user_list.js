var csrftoken = getCookie('csrftoken');
$(document).on('click', '.user-status', function(){
	var status = $(this).attr("data-status");
	var user_id = $(this).attr("data-user-id");
	$.ajax({
		type: 'POST',
		url: URLS.ajax_user_status,
		beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
          },
		data: {'status': status, 'user_id':user_id},
		success: function(response){
			if(response.status == "Deactive"){
				$("#user_status_"+response.userId).removeClass("label-success");
				$("#user_status_"+response.userId).addClass("label-danger");
			}else{
				$("#user_status_"+response.userId).removeClass("label-danger");
				$("#user_status_"+response.userId).addClass("label-success");
			}
			$("#user_status_"+response.userId).text(response.status);
			$("#user_status_"+response.userId).attr("data-status", response.status);
			var message_dialog = $("#message-dialog");
	        message_dialog.find('p strong').html('User is successfully '+response.status+'!!');
	        message_dialog.show();
	        $(window).scrollTop($('#message-dialog').offset().top);
	        message_dialog.fadeOut(10000);
		}
	})
});
