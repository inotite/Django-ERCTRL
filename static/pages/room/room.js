 $(".setting").click(function(){
      $(".setting_drop_down").slideToggle('slow');
  });
  $(".notifation").click(function(){
      $(".notification_drop_down").slideToggle('slow');
  });

  // Add js for loader
  $("#spin").spinner({
      color: "black"
      , background: "rgba(255,255,255,0.5)"
      , html: "<i class='fa fa-repeat' style='color: gray;'></i>"
      , spin: true
    });

  // Added js for create clue
  $(document).on("submit", "#clue-form", function (e) {
      e.preventDefault();
      var create_clue = $("#clue-form");
      var url = create_clue.attr('action'),
              data = create_clue.serialize();
      $("#spin").show();
      $.ajax({
          type: "POST",
          url: url,
          data: data,
          success: function (data) {
            $(".clue-info-table").html(data['clue_data']);
            $("#spin").hide();
            var message_dialog = $("#message-dialog");
            message_dialog.find('p strong').html('Successfully saved');
            message_dialog.show();
            $(window).scrollTop($('#message-dialog').offset().top);
            message_dialog.fadeOut(10000);
            $("#id_name").val('');
          }
      });
      return false;
  });

  // Delete clue js
  $(document).on('click', '.actions-clue-td a.delete-clue-a', function (e) {
    var link = $(this);
    e.stopPropagation();
    e.preventDefault();
    $.confirm({
      'text': '<b>Are you sure?</b>',
      confirm: function () {
          $.ajax({
              type: "POST",
              url: URLS.clue_delete,
              beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
              },
              data: {
                  'clue_id': link.attr('data-id')
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

  // Edit clue js
  $(document).on("click", ".edit-question", function () {
    var elm = $(this),
            tr_elm = elm.parents('tr'),
            p = tr_elm.find('td p');
    p.after(function () {
        return "<input type='text' class='form-control inline-que-edit' value='" + p.text() + "'/>"
    });
    elm.parents("tr").find("td:nth-child(2) a:nth-child(2) i").removeClass('glyphicon-edit-clue');
    elm.parents("tr").find("td:nth-child(2) a:nth-child(2) i").removeClass('glyphicon-edit');
    elm.parents("tr").find("td:nth-child(2) a:nth-child(2) i").addClass('glyphicon-ok-circle');
    p.hide();
  });

  // Edit clue js
  $(document).on("click", ".glyphicon-edit-clue", function () {
    var elm = $(this),
            tr_elm = elm.parents('tr'),
            p = tr_elm.find('td:first p');
    p.after(function () {
        return "<input type='text' class='form-control inline-que-edit' value='" + p.text() + "'/>"
    });
    elm.removeClass('glyphicon-edit-clue');
    elm.parents("tr").find("td:nth-child(2) a:nth-child(2) i").removeClass('glyphicon-edit');
    elm.parents("tr").find("td:nth-child(2) a:nth-child(2) i").addClass('glyphicon-ok-circle');
    p.hide();
  });

  // using jQuery
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  // Update clue js
  $(document).on("click", ".glyphicon-ok-circle", function () {
    var elm = $(this),
            tr_elm = elm.parents('tr'),
            p = tr_elm.find('td:nth-child(1) p'),
            input = tr_elm.find('td:nth-child(1) .inline-que-edit');
    // var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $("#spin").show();
    if (input.val() != p.text()) {
      $.ajax({
        // csrfmiddlewaretoken: csrf_token,
        type: "POST",
        url: URLS.clue_edit,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        data: {
            'name': input.val(),
            'id': tr_elm.data("clue-id")
        },
        success: function (res) {
          p.text(input.val());
          input.remove();
          p.show();
          elm.removeClass('glyphicon-ok-circle');
          elm.addClass('glyphicon-edit');
          elm.addClass('glyphicon-edit-clue');
          var message_dialog = $("#message-dialog");
          message_dialog.find('p strong').html('Successfully updated');
          message_dialog.show();
          $("#spin").hide();
          $(window).scrollTop($('#message-dialog').offset().top);
          message_dialog.fadeOut(10000);
        }
      });
    } else {
      elm.removeClass('glyphicon-ok-circle');
      elm.addClass('glyphicon-edit');
      elm.addClass('glyphicon-edit-clue');
      input.remove();
      p.show();
      $("#spin").hide();
    }
  });

  // Add image for js
  $(document).on("submit", "#image-form", function (e) {
      var create_image = $("#image-form");
      $("#spin").show();
      var data = new FormData(create_image.get(0));
      var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
      data['room'] = $("#id_room").val()
      $.ajax({
          csrfmiddlewaretoken: csrf_token,
          url: URLS.room_create_image,
          type: 'POST',
          data: data,
          enctype: "multipart/form-data",
          processData: false,
          contentType: false,
          cache: false,
          success: function (response) {
            $(".image-info-table").html(response['images_data']);
            $("#spin").hide();
            var message_dialog = $("#message-dialog");
            $(".help-block-img-name").remove();
            if (response['status'] == 'ok'){
              message_dialog.find('p strong').html(response['messages']);
              message_dialog.show();
              $(window).scrollTop($('#message-dialog').offset().top);
              message_dialog.fadeOut(10000);
            }else{
              var img_name = $("#id_img_name");
              if (img_name.parent().find(".help-block-img-name").length < 1){
                img_name.after('<ul class="help-block help-block-img-name"><li>'+response['messages']+'.</li></ul>')
              }
            }
            $("#id_img_name").val('');
          },
          error: function (res) {
            alert("Error: " + res.responseText);
          }
      });
      return false;
  });

  // Delete image for js
  $(document).on('click', '.actions-image-td a.delete-image-a', function (e) {
    var link = $(this);
    e.stopPropagation();
    e.preventDefault();
    $.confirm({
      'text': '<b>Are you sure?</b>',
      confirm: function () {
          $.ajax({
              type: "POST",
              url: URLS.image_delete,
              beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
              },
              data: {
                  'image_id': link.attr('data-id')
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

  // Add sound for js
  $(document).on("submit", "#sound-form", function (e) {
      var create_sound = $("#sound-form");
      var data = new FormData(create_sound.get(0));
      var room_id = $("#id_room").val();
      var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
      data['name'] = $(this).find("#id_name").val();
      $("#spin").show();
      $.ajax({
          csrfmiddlewaretoken: csrf_token,
          url: URLS.dashboard_rooms_sound_create.replace("111111", room_id),
          type: 'POST',
          data: data,
          enctype: "multipart/form-data",
          processData: false,
          contentType: false,
          cache: false,
          success: function (response) {
            // $('#loading').hide();
            $("#spin").hide();
            $(".sound-info-table").html(response.sounds_data);
            var message_dialog = $("#message-dialog");
            $(".help-block-sound-name").remove();
            if (response.status == 'ok'){
              message_dialog.find('p strong').html(response.messages);
              message_dialog.show();
              $(window).scrollTop($('#message-dialog').offset().top);
              message_dialog.fadeOut(10000);
            }else{
              var img_name = $("#id_sound_img");
              if (img_name.parent().find(".help-block-sound-name").length < 1){
                img_name.after('<ul class="help-block help-block-sound-name"><li>'+response.messages+'.</li></ul>')
              }
            }
            $("#id_sound_img").val('');
            $("#id_name").val('');
          },
          error: function (res) {
            alert("Error: " + res.responseText);
          }
      });
      return false;
  });


  // Delete image for js
  $(document).on('click', '.actions-sound-td a.delete-sound-a', function (e) {
    var link = $(this);
    e.stopPropagation();
    e.preventDefault();
    var room_id = $(this).data("room-id");
    var sound_id = $(this).data("id");
    $.confirm({
      'text': '<b>Are you sure?</b>',
      confirm: function () {
          $.ajax({
              type: "POST",
              url: URLS.dashboard_rooms_sound_delete.replace("222222",sound_id),
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

  // Add video for js
  $(document).on("submit", "#video-form", function (e) {

      $("#spin").show();
      var create_video = $("#video-form");
      var data = new FormData(create_video.get(0));
      var room_id = $("#id_room").val();
      var csrf_token = $('#video-form input[name="csrfmiddlewaretoken"]').val();
      data['name'] = $(this).find("#id_name").val();
      $.ajax({
          csrfmiddlewaretoken: csrf_token,
          url: URLS.dashboard_rooms_video_create.replace("4444444", room_id),
          type: 'POST',
          data: data,
          enctype: "multipart/form-data",
          processData: false,
          contentType: false,
          // cache: false,
          success: function (response) {
            $(".video-info-table").html(response.videos_data);
            $("#spin").hide();
            var message_dialog = $("#message-dialog");
            $(".help-block-video-name").remove();
            if (response.status == 'ok'){
              message_dialog.find('p strong').html(response.messages);
              message_dialog.show();
              $(window).scrollTop($('#message-dialog').offset().top);
              message_dialog.fadeOut(10000);
            }else{
              var video_name = $("#id_video_img");
              if (video_name.parent().find(".help-block-video-name").length < 1){
                video_name.after('<ul class="help-block help-block-video-name"><li>'+response.messages+'.</li></ul>')
              }
            }
            $("#id_video_img").val('');
            $("#id_name").val('');
          },
          error: function (res) {
            alert("Error: " + res.responseText);
          }
      });
      return false;
  });
  
  // Delete video for js
  $(document).on('click', '.actions-video-td a.delete-video-a', function (e) {
    var link = $(this);
    e.stopPropagation();
    e.preventDefault();
    var room_id = $(this).data("room-id");
    var video_id = $(this).data("id");
    var csrf_token = $('#video-form input[name="csrfmiddlewaretoken"]').val();
    $.confirm({
      'text': '<b>Are you sure?</b>',
      confirm: function () {
          $.ajax({
              csrfmiddlewaretoken: csrf_token,
              type: "POST",
              url: URLS.dashboard_rooms_video_delete.replace("333333",video_id),
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

  // Added js for create puzzle
  $(document).on("submit", "#puzzle-form", function (e) {
      e.preventDefault();
      var create_puzzle = $("#puzzle-form");
      var url = create_puzzle.attr('action'),
              data = create_puzzle.serialize();
      var csrf_token = $('#puzzle-form input[name="csrfmiddlewaretoken"]').val();
      var room_id = $("#id_room").val();
      $("#spin").show();
      $.ajax({
          csrfmiddlewaretoken: csrf_token,
          type: "POST",
          url: URLS.dashboard_rooms_puzzle_create.replace("111111", room_id),
          data: data,
          success: function (response) {
            var message_dialog = $("#message-dialog");
            $(".puzzle-info-table").html(response.puzzles_data);
            $("#spin").hide();
            message_dialog.find('p strong').html(response.messages);
            message_dialog.show();
            $(window).scrollTop($('#message-dialog').offset().top);
            message_dialog.fadeOut(10000);
            $("#id_puzzle_name").val('');
            $("#id_reset_instructions").val('');
            $("#id_damage_or_notes").val('');
          }
      });
      return false;
  });

  // Delete puzzle for js
  $(document).on('click', '.actions-puzzle-td a.delete-puzzle-a', function (e) {
    var link = $(this);
    e.stopPropagation();
    e.preventDefault();
    var room_id = $(this).data("room-id");
    var puzzle_id = $(this).data("id");
    var csrf_token = $('#puzzle-form input[name="csrfmiddlewaretoken"]').val();
    $.confirm({
      'text': '<b>Are you sure?</b>',
      confirm: function () {
          $.ajax({
              csrfmiddlewaretoken: csrf_token,
              type: "POST",
              url: URLS.dashboard_rooms_puzzle_delete.replace("333333",puzzle_id),
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

  $(document).on("click", ".edit-puzzle-a", function (e) {
    // e.preventDefault();
    var puzzle_id = $(this).data("id");
    var room_id = $(this).data("room-id");
    $("#spin").show();
    $.ajax({
          type: "GET",
          url: URLS.dashboard_rooms_puzzle_edit.replace("333333", room_id).replace("444444", puzzle_id),
          processData: false,
          contentType: false,
          success: function (response) {
            $("#panel-body-"+puzzle_id).html(response);
            puzzle_form_hide_or_show(puzzle_id);
            $("#spin").hide();
            validate_puzzle_form(puzzle_id);
          }
    });
  });

  function validate_puzzle_form(puzzle_id) {
      // Add validation on resource upload form
      $("#id-puzzle-update-"+puzzle_id).validate({
          // Specify the validation rules
          rules: {
              puzzle_name: "required",
              reset_instructions: "required"
          },

          // Specify the validation error messages
          messages: {
              puzzle_name: "This field may not be blank.",
              reset_instructions: "This field may not be blank."
          },
          submitHandler: function (form) {
            var data = new FormData(form);
            var csrf_token = form.elements.csrfmiddlewaretoken.value;
            var puzzle_id = form.getAttribute('data-puzzle-id');
            var room_id = form.getAttribute('data-room-id');
            var new_url  = URLS.dashboard_rooms_puzzle_edit.replace("333333", room_id).replace("444444", puzzle_id);
            $("#spin").show();
            $.ajax({
                csrfmiddlewaretoken: csrf_token,
                type: "POST",
                url: new_url,
                data: data,
                processData: false,
                contentType: false,
                success: function (response) {
                  var message_dialog = $("#message-dialog");
                  if (response.status == 'ok'){
                    $(".puzzle-info-table").html(response.puzzles_data);
                    message_dialog.find('p strong').html(response.messages);
                    message_dialog.show();
                    $(window).scrollTop($('#message-dialog').offset().top);
                    message_dialog.fadeOut(10000);
                    $("#id-puzzle-update-"+ puzzle_id).find("#id_puzzle_name").val('');
                    $("#id-puzzle-update-"+ puzzle_id).find("#id_reset_instructions").val('');
                    $("#id-puzzle-update-"+ puzzle_id).find("#id_damage_or_notes").val('');
                  }else{
                    $("#id-puzzle-update-"+ puzzle_id).find(".help-block").remove();
                    if(response.messages.puzzle_name != undefined){
                      $("#id-puzzle-update-"+ puzzle_id).find("#id_puzzle_name").after('<ul class="help-block error-block-puzzle-name"><li>'+response.messages.puzzle_name+'</li></ul>');
                    }
                    if(response.messages.reset_instructions != undefined){
                      $("#id-puzzle-update-"+ puzzle_id).find("#id_reset_instructions").after('<ul class="help-block error-block-reset-instructions"><li>'+response.messages.reset_instructions+'</li></ul>');
                    }
                  }
                  $("#spin").hide();
                   return false;
                }
            });
          }
      });
  }

  function puzzle_form_hide_or_show(puzzle_id){
    $('#panel-default-'+puzzle_id).on('hidden.bs.collapse', function (e) {
      $("#puzzle-name-"+puzzle_id).show();
      $("#glyphicon-move-"+puzzle_id).show();
      $("#id-edit-puzzle-"+puzzle_id).html('<span class="glyphicon glyphicon-chevron-up"></span> Edit');
    });
    $('#panel-default-'+puzzle_id).on('shown.bs.collapse', function () {
      $("#puzzle-name-"+puzzle_id).hide();
      $("#glyphicon-move-"+puzzle_id).hide();
      $("#id-edit-puzzle-"+puzzle_id).html('<span class="glyphicon glyphicon-chevron-down"></span> Edit');
    });
  }

  $(function () {
    var tabContainers = $('div.tabs > div');
    tabContainers.hide().filter(':first').show();
    $('div.tabs ul.tab-nav a').click(function () {
      tabContainers.hide();
      tabContainers.filter(this.hash).show();
      $('div.tabs ul.tab-nav a').removeClass('selected');
      $(this).addClass('selected');
      return false;
    }).filter(':first').click();
});

// Display theme image according to theme selection
$("#id_theme").change(function(){
  var theme_val = $(this).find("option:selected").text().toLowerCase();
  var new_img_url = "/static/vendor/bootstrap/images/"+theme_val+"_demo.png"
  $(".display-theme-image img").attr("src", new_img_url);
});

var live_view_font_val = $("#id_live_view_font option:selected").data("value");
display_live_view_font_by_font_family(live_view_font_val)
$(document).on("change", "#id_live_view_font", function () {
  var optionSelected = $(this).find('option:selected').attr("data-value");
  display_live_view_font_by_font_family(optionSelected)
});

function display_live_view_font_by_font_family(optionSelected){
  $('.font-preview').css("font-family", optionSelected);
}