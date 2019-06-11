// Delete room js
var csrftoken = getCookie('csrftoken');

$(document).on('click', '.delete-tablet-room', function (e) {
  var link = $(this);
  e.stopPropagation();
  e.preventDefault();
  $.confirm({
    'text': '<b>Are you sure?</b>',
    confirm: function () {
        $.ajax({
            type: "POST",
            url: URLS.guide_dashboard_rooms_delete.replace("111111", link.attr('data-room-id')),
            beforeSend: function(xhr, settings) {
              if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
              }
            },
            success: function (res) {
              link.parents(".darhboard_box").remove();
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


function puzzle_delete(event){
 action = event.action;
 puzzle_id = event.action.split('puzzles')[1].split('/')[1];
 $.ajax({
    type:"POST",
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
    url: action,
    data: puzzle_id,
    success:function(response){
      $("tr[data-puzzle-id='" + puzzle_id +"']").remove();
    }
  });
  return false;
};
function jQFormSerializeArrToJson(formSerializeArr){
  var jsonObj = {};
  jQuery.map( formSerializeArr, function( n, i ) {
    jsonObj[n.name] = n.value;
  });

 return jsonObj;
}

function IsAlphaOrIsNumeric(str) {
  return /^(?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9]+)$/.test(str);
}

$(document).on("submit", "#edit-puzzle-form", function (e) {
  e.preventDefault();
  var puzzle_clue = $("#edit-puzzle-form");
  var room_id = $(object_id).attr('value');
  var url = '/dashboard/rooms/'+room_id+'/puzzle/create/',
          data = puzzle_clue.serialize();
  $("#spin").show();
  $.ajax({
      type: "POST",
      url: url,
      data: data,
      success: function (data) {
        $(".puzzles-info-table").html(data['puzzles_data']);
        $("#spin").hide();
        var message_dialog = $("#message-dialog");
        message_dialog.find('p strong').html('Successfully saved');
        message_dialog.show();
        $(window).scrollTop($('#message-dialog').offset().top);
        message_dialog.fadeOut(10000);
      }
  });
    return false;
});

$(document).on("submit","#edit-scoring-form",function(event){
  event.preventDefault();
  var form = $(this);
  var action = form.attr('action');
  var serializedArr = form.serializeArray();
  var properJsonObj = jQFormSerializeArrToJson(serializedArr);
  $.ajax({
    type:"POST",
    url: action,
    data: properJsonObj,
    success:function(response){
      $('.scoring-tab').html(response)
      alert('Data is Saved')
    }
  });
  return false;
});

// this Jquery is used for admin_pin validation
// $(document).on("submit","#edit-room-form",function(event){
//   var admin_pin = $('#id_admin_pin').val()
//   if(IsAlphaOrIsNumeric(admin_pin) == false){
//     if($.isNumeric(admin_pin) == false){
//         $("#admin_error").append("<p>Enter a valid value. </p>");
//         event.preventDefault();
//     }
//   }
//   if (admin_pin.length < 4){
//     $("#admin_error").append("<p>Ensure this value has at least 4 characters.(it has " + admin_pin.length +") </p>");
//     event.preventDefault();
//   }
// });

$(document).on("click",".clue_edit",function(){
  var clue_id = $(this).attr("value");
  $(".clue_id").trigger("change");
  if($('.edit-clue').hasClass('in')){
  $('.edit-clue').removeClass('in');
  }
});

$(document).on("change",".clue_id",".clue_edit",function(){
  var puzzleid = $(".puzzle_id").attr("value"),
  clue_id = $(this).attr("value"),
  clue_icon_value = $('.clue_icon_'+clue_id).attr("value"),
  clue_textarea_value = $('.clue_textarea_'+clue_id).attr("value");
  var clue_icon = (!!clue_icon_value) ? clue_icon_value : "";
  var clue_textarea = (clue_textarea_value != "None") ? clue_textarea_value : "";
  try {
    var clue_file_uploads = $('.clue_file_uploads_'+clue_id).attr("value").split("/").pop();
  }
  catch(err) {
    var clue_file_uploads = "";
  }

  if($('option:selected','.clue_file_type_'+clue_id).attr("value") == 'Text'){
    add_or_remove(clue_id);
    add_text(clue_id, clue_textarea, clue_icon,puzzleid);
  }

  if($('option:selected','.clue_file_type_'+clue_id).attr("value") == 'Image'){
    add_or_remove(clue_id);
    add_image(clue_id, clue_file_uploads, clue_icon,puzzleid);
  }

  if($('option:selected','.clue_file_type_'+clue_id).attr("value") == 'Audio'){
    add_or_remove(clue_id);
    add_audio(clue_id, clue_file_uploads, clue_icon,puzzleid);
  }

  if($('option:selected','.clue_file_type_'+clue_id).attr("value") == 'Video'){
    add_or_remove(clue_id);
    add_video(clue_id, clue_file_uploads, clue_icon,puzzleid);
  }
});
function add_text(clue_id, clue_textarea, clue_icon,puzzleid){
  $('#panel-body_'+clue_id).append('<div id="spin"></div>  <div id="message-dialog" class="alert alert-success" style="bottom: 10px; right: 20px; display: none; z-index: 4000"><p> <strong></strong></p></div><div id=textarea_'+clue_id+' class="puzzle_textSelect"><form  id="clue-form" method=POST" enctype="multipart/form-data" onchange="clue_function(this)" action="/guide/rooms/'+puzzleid+'/puzzleclue/add"> <input type="Hidden" name="clue_uploads_options" value="Text"><input type="hidden" name="clue_checkbox" value = "on"><input type="hidden" name="clue_id" value="'+clue_id+'"><div class="pzlclue_textarea"><textarea name = "clue_textarea" id="clue_'+clue_id+'" cols="150" rows="4" id="id_clue_textarea" required>'+clue_textarea+'</textarea></div></form><form  id="clue-form" method=POST" enctype="multipart/form-data" onchange="clue_function(this)" action="/guide/rooms/'+puzzleid+'/puzzleclue/add"> <div class="show-Dash-icon"><input type="hidden" name="clue_id" value="'+clue_id+'"><a class = "clue_icon_'+clue_id+'"  style="color: red" href = "'+clue_icon+'" ></a><label>Clue Icon : </label><span class="dashIcon_img"><img id = "clue_icon_'+clue_id+'" src = '+clue_icon+'></span></div><div class="choose-icon"><input type="file" name="clue_icon"><span class= "clue_error_msg'+clue_id+'" style="color:red"  ></span></div></form></div>');
}
function add_image(clue_id, clue_file_uploads, clue_icon,puzzleid){
  $('#panel-body_'+clue_id).append('<div id="spin"></div>  <div id="message-dialog" class="alert alert-success" style="bottom: 10px; right: 20px; display: none; z-index: 4000"><p> <strong></strong></p></div><div id= "image_'+clue_id+'"><form id="clue-form" class="puzzle_imageSelect"  method=POST" onchange="clue_function(this)" action="/guide/rooms/'+puzzleid+'/puzzleclue/add"><input type="Hidden" name="clue_uploads_options" value="Image"><input type="hidden" name="clue_checkbox" value = "on"><input type="hidden" name="clue_id" value="'+clue_id+'"><div class="plz_file_uploads"><label>Image : </label><span class="plz_imgView"><img id = "span_clue_file_uploads_'+clue_id+'" src = "/media/avatars/'+clue_file_uploads+'"></span><input type="file" name="clue_file_uploads"></div> <span style ="color:red" class = "error_msg_'+clue_id+'" ></span> <div class="show-Dash-icon"><a class = "clue_icon_'+clue_id+'"  style="color: red" href = "'+clue_icon+'" ></a><label>Clue Icon : </label><span class="dashIcon_img"><img id = "clue_icon_'+clue_id+'" src = '+clue_icon+'></span></div><div class="choose-icon"><label>Change : </label> <input type="file" name="clue_icon"><span class= "clue_error_msg'+clue_id+'" style="color:red" ></span></div></form></div>')
}

function add_audio(clue_id, clue_file_uploads, clue_icon,puzzleid){
  var file_type = 'Audio';
  var clue_file_uploads = audio_video_display_validation(clue_id,file_type,clue_file_uploads);
  $('#panel-body_'+clue_id).append('<div id="spin"></div>  <div id="message-dialog" class="alert alert-success" style="bottom: 10px; right: 20px; display: none; z-index: 4000"><p> <strong></strong></p></div><div  id= "audio_'+clue_id+'"><form id="clue-form" class="puzzle_audioSelect"  method=POST" onchange="clue_function(this)" action="/guide/rooms/'+puzzleid+'/puzzleclue/add"> <input type="hidden" name="clue_checkbox" value = "on"><input type="Hidden" name="clue_uploads_options" value="Audio"><span class="plz_imgView" id = "span_clue_file_uploads_'+clue_id+'" ></span><input type="hidden" name="clue_id" value="'+clue_id+'"><br /><div class="plz_file_uploads"><label>Audio: </label> <span class = "plz_file" id = "span_audio_'+clue_id+'" title="'+clue_file_uploads+'">'+clue_file_uploads +'</span> value <input type="file" name="clue_file_uploads"  ><br/><span class = "error_msg_'+clue_id+'" style = "color:red"></span></div> <div class="show-Dash-icon"><a class = "clue_icon_'+clue_id+'"  style="color: red" href = "'+clue_icon+'" ></a><label>Clue Icon : </label><span class="dashIcon_img"><img id = "clue_icon_'+clue_id+'" src = '+clue_icon+'></span></div><div class="choose-icon"><label>Change : </label> <input type="file" name="clue_icon"><span class= "clue_error_msg'+clue_id+'" style="color:red" ></span></div></form></div>')
}

function add_video(clue_id, clue_file_uploads, clue_icon,puzzleid){
  var file_type = 'Video';
  var clue_file_uploads = audio_video_display_validation(clue_id,file_type,clue_file_uploads);
  $('#panel-body_'+clue_id).append('<div id="spin"></div>  <div id="message-dialog" class="alert alert-success" style="bottom: 10px; right: 20px; display: none; z-index: 4000"><p> <strong></strong></p></div><div id= "video_'+clue_id+'"><form id="clue-form" class="puzzle_videoSelect"  method=POST" onchange="clue_function(this)"action="/guide/rooms/'+puzzleid+'/puzzleclue/add">   <input type="Hidden" name="clue_uploads_options" value="Video"><span class="plz_imgView" id = "span_clue_file_uploads_'+clue_id+'" ></span><input type="hidden" name="clue_id" value="'+clue_id+'"><br /><div class="plz_file_uploads"><label>Video: </label> <span class = "plz_file" id = "span_video_'+clue_id+'" title="'+clue_file_uploads+'">'+clue_file_uploads +'</span> <input type="file" name="clue_file_uploads"> <br/><span class = "error_msg_'+clue_id+'" style = "color:red"> </span> </div> <div class="show-Dash-icon"><a class = "clue_icon_'+clue_id+'"  style="color: red" href = "'+clue_icon+'" ></a><label>Clue Icon : </label><span class="dashIcon_img"><img id = "clue_icon_'+clue_id+'" src = '+clue_icon+'></span></div><div class="choose-icon"><label>Change : </label> <input type="file" name="clue_icon"><span class= "clue_error_msg'+clue_id+'" style="color:red" ></span></div></form></div>')
}

function add_or_remove(clue_id){
  $('#textarea_'+clue_id).remove();
  $('#image_'+clue_id).remove();
  $('#audio_'+clue_id).remove();
  $('#video_'+clue_id).remove();
  if($('.edit-clue').hasClass('in')){
    $('.edit-clue').removeClass('in');
  }
  $('#collapse_'+clue_id).addClass('in');
}

function audio_video_display_validation(clue_id,file_type,file_value){
 var new_file_value = file_value;
  if(file_type == 'Audio'){
    regex = new RegExp("(.?)\.(mp3)");
    if(!(regex).test(file_value)){
      return  new_file_value = '';
    }
    else{
      $('#span_audio_'+clue_id).text(new_file_value);
      return new_file_value;
    }
  }
  if(file_type == 'Video'){
    regex = new RegExp("(.?)\.(mp4)");
    if(!(regex).test(file_value)){
      return new_file_value = ''
    }
    else{
      $('#span_video_'+clue_id).text(new_file_value);
      return new_file_value;
    }
  }
}

function file_input_validation(file_type,file_value,clue_id){

  if(file_type == 'Image'){
    regex = new RegExp("(.?)\.(jpg|png|gif)")
    $('.error_msg_'+clue_id).text('');
    if(!(regex).test(file_value)){
      var msg = 'File type not supported! File must be .jpg or .png or .gif'
      $('.error_msg_'+clue_id).text(msg);
      return false;
    }
    else{
      return true;
    }
  }

  if(file_type == "Audio"){
    regex = new RegExp("(.?)\.(mp3)");
    $('.error_msg_'+clue_id).text('');
    if(!(regex).test(file_value)){
      var msg = 'File type not supported! File must be .mp3';
      $('.error_msg_'+clue_id).text(msg);
      return false;
    }
    else{
      return true;
    }
  }

  if(file_type == "Video"){
    regex = new RegExp("(.?)\.(mp4)");
    $('.error_msg_'+clue_id).text('');
    if(!(regex).test(file_value)){
      var msg = 'File type not supported! File must be .mp4';
      $('.error_msg_'+clue_id).text(msg);
      return false;
    }
    else{
      return true;
    }
  }
  if(file_type == 'clue_icon'){
    regex = new RegExp("(.?)\.(jpg|png|gif)")
    $('.clue_error_msg'+clue_id).text('');
    if(!(regex).test(file_value)){
      $('.clue_error_msg'+clue_id).text('');
      msg = 'File type not supported! File must be .jpg or .png or .gif'
      $('.clue_error_msg'+clue_id).text(msg);
      return false
    }
    else{
      return true
    }
  }
  if(file_type == 'dashboard_icon'){
    regex = new RegExp("(.?)\.(jpg|png|gif)");
    if(!(regex).test(file_value)){
      $('.clue_error_msg'+clue_id).text('');
      msg = 'File type not supported! File must be .jpg or .png or .gif'
      // alert('stop');
      $("#spin").hide();
      var message_dialog = $('.error-message-dialog_'+clue_id);
      message_dialog.find('p strong').html('File type not supported! File must be .jpg or .png or .gif');
      message_dialog.show();
      $(window).scrollTop(message_dialog.offset().top);
      message_dialog.fadeOut(10000);
      return false;
    }
    else{
      return true;
    }
  }
}

function clue_function(event){
  var csrftoken = getCookie('csrftoken'),
  form = new FormData(event),
  action = event.action,
  clue_id = event.elements.clue_id.defaultValue,
  file_validation = true,file_validation_clue = true;
  if ('clue_uploads_options' in event.elements){
    var clue_uploads_options = $("input[name='clue_uploads_options']").val(),
    clue_file_uploads = $( "input[name='clue_file_uploads']").val();
    if (clue_file_uploads) {
    file_validation =file_input_validation(clue_uploads_options,clue_file_uploads,clue_id);
    }
  }
  if (('clue_icon' in event.elements)){
    var clue_type = 'clue_icon',
    clue_icon_value = $('input[name=clue_icon]').val();
    if (clue_icon_value) {
      file_validation_clue =file_input_validation(clue_type,clue_icon_value,clue_id);
    }
  }
  if (file_validation && file_validation_clue){
    $("#spin").show();
    $.ajax({
      type:"POST",
      url: action,
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      },
      data: form,
      processData: false,
      contentType: false,
      cache:false,
      success:function(response){
        $("#spin").hide();
        var message_dialog = $("#message-dialog");
        message_dialog.find('p strong').html('Successfully saved');
        message_dialog.show();
        $(window).scrollTop($('#message-dialog').offset().top);
        message_dialog.fadeOut(10000);
        //File Uploads
        if (response['file_upload_type']== 'clue_file_upload'){
          $('#span_clue_file_uploads_'+response['clue_id']).attr("src",response['data']);
          $('#clue_'+response['clue_id']).attr("href",response['data']);
          $('#clue_file_uploads_text_'+response['clue_id']).text(response['data']);
          $('#span_audio_'+response['clue_id']).text(response['data']);
          $('#span_video_'+response['clue_id']).text(response['data']);
        }
        // Clue Icon
        if (response['file_upload_type']== 'clue_icon') {
          $('.clue_icon_'+response['clue_id']).attr("href",response['data']);
          $('.clue_icon_'+response['clue_id']).attr("value",response['data']);
          $('#clue_icon_'+response['clue_id']).attr("src",response['data']);
        }
        // Textarea
        var textarea = JSON.parse(response);
        $('#clue_'+textarea['clue_id']).val(textarea['data']);
        $('.clue_textarea_'+textarea['clue_id']).attr("value",textarea['data']);
      }
    });
  }
return false;
};

function clue_options(event){
  var csrftoken = getCookie('csrftoken'),
  form = new FormData(event),
  action = event.action;
  puzzle_id = event.action.split('rooms')[1].split("/")[1];
  file_validation = true
  dashboard_icon_value= $("input[name='dashboard_icon']").val();
  if ('dashboard_icon' in event.elements){
    // var dashboard_icon_value= $( "input[name='dashboard_icon']").val(),
    var dashboard_icon_type = 'dashboard_icon';
    if (dashboard_icon_value){
      file_validation = file_input_validation(dashboard_icon_type,dashboard_icon_value,puzzle_id);
    }
  }
  $("#spin").show();
  if(file_validation){
    $.ajax({
      type:"POST",
      url: action,
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      },
      data: form,
      processData: false,
      contentType: false,
      cache:false,
      success:function(response){
        $("#spin").hide();
        var message_dialog = $("#message-dialog");
        message_dialog.find('p strong').html('Successfully saved');
        message_dialog.show();
        $(window).scrollTop($('#message-dialog').offset().top);
        message_dialog.fadeOut(10000);
        $('#dashboard_icon_'+response['puzzle_id']).attr("src",response['data']);
        if (response['data'] == null){
          $('.icon_clear').css('display','none');
          $("#icon_clear_checkbox").attr('checked',false);
        }
        else{
          $('.icon_clear').css('display','inline');
        }
      }
    });
  }
 return false;
};
