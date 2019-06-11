var csrftoken = getCookie('csrftoken');
// Display fields and help message according to event selection
$(document).on('click', '#event-type', function(){
// $("#event-type").change(function(){
  var event_type  = $(this).find("option:selected").text();
  get_attribute_by_event(event_type);
});

function get_attribute_by_event(event_type){
  if (event_type == "Time Elapsed"){
    event_time_elapsed();
  }
  if (event_type == "Network Polling (Listen for Prop)"){
    event_network_polling();
  }
  if (event_type == "Custom Button"){
    event_custom_button();
  }
  if (event_type == "Custom Event"){
    event_event_name();
  }
  if (event_type == "Timer Started"){
    var help_message = "Trigger actions when the timer is started";
    replace_help_message_and_event_fields(help_message, "");
  }
  if (event_type == "Timer Stopped"){
    var help_message = "Trigger actions when the timer is stopped";
    replace_help_message_and_event_fields(help_message, "");
  }
  if (event_type == "Room Completed"){
    var help_message = "Trigger actions when the room has been successfully completed";
    replace_help_message_and_event_fields(help_message, "");
  }
  if (event_type == "Room Failed"){
    var help_message = "Trigger actions when the timer has run out and the players and failed to complete the room";
    replace_help_message_and_event_fields(help_message, "");
  }
  if (event_type == "Room Reset"){
    var help_message = "Trigger actions when the room is reset such resetting a prop";
    replace_help_message_and_event_fields(help_message, "");
  }
}

// Add multiple action form for js
$(document).on('click', '.add-multiple-action-form', function(){
  var item = _.template($("#automation-action-form-tpl").html() );
  $(".action-box-body").append(item);
  if($(".action-box-body .page_form").length > 1){
    var html_delete_btn = '<div class="page_form_field"><button class="red_btn remove-action-form">Delete</button></div>'
    $(".action-box-body .page_form").each(function(){
      if(!$(this).find("button").hasClass("remove-action-form")){
        $(this).append(html_delete_btn);
      }
    }) ;
  }
});

// Remove action form for js
$(document).on('click', '.remove-action-form', function(){
  $(this).parents(".page_form").remove();
  if ($(".action-box-body .page_form").length < 2){
    $(".action-box-body .page_form .remove-action-form").remove();
  }
});

if(isCreate){
  get_attribute_by_event($("#event-type").find("option:selected").text());
  get_attribute_by_action($(".event-action option:first"), $(".event-action option:first").text());
}

// Display fields and help message according to action selection
$(document).on('change', '.event-action', function(){
  var action_obj = $(this);
  var event_action = $(this).find("option:selected").text();
  get_attribute_by_action(action_obj, event_action);
});

function get_attribute_by_action(action_obj, event_action){
  if (event_action == "Send Clue Text"){
    action_send_clue_text(action_obj);
  }
  if (event_action == "Play Alert Tone"){
    var help_message = "Play the default room alert tone used when sending clues";
    replace_help_message_and_action_fields(help_message, "", action_obj);
  }
  if (event_action == "Play Sound"){
    action_play_sound(action_obj);
  }
  if (event_action == "Play Video"){
    action_play_video(action_obj);
  }
  if (event_action == "Display Image"){
    action_display_images(action_obj);
  }
  if (event_action == "Send Network Request (Trigger Prop)"){
    action_send_network_request(action_obj);
  }
  if (event_action == "Complete Puzzle"){
    action_complete_puzzle_request(action_obj);
  }
  if (event_action == "Philips Hue Lights Scene"){
    action_philips_hue_lights_group_and_scene_request(action_obj);
  }
  if (event_action == "Philips Hue Lights Blink"){
    action_philips_hue_lights_blink_request(action_obj);
  }
  if (event_action == "Philips Hue Lights on/off"){
    action_philips_hue_lights_on_or_off_request(action_obj);
  }
  if (event_action == "Start Timer"){
    var help_message = "Begin the countdown timer";
    replace_help_message_and_action_fields(help_message, "", action_obj);
  }
  if (event_action == "Stop Timer"){
    var help_message = "Stop the countdown timer (but do not complete or fail the room)";
    replace_help_message_and_action_fields(help_message, "",action_obj);
  }
  if (event_action == "Adjust Time"){
    action_adjust_time_request(action_obj);
  }
  if (event_action == "Complete Room"){
    var help_message = "Stop the timer and complete the room (the group wins!)";
    replace_help_message_and_action_fields(help_message, "", action_obj);
  }
  if (event_action == "Fail Room"){
    var help_message = "Stop the timer and fail the room (the group loses)";
    replace_help_message_and_action_fields(help_message, "",action_obj);
  }
  if (event_action == "Reset Room"){
    var help_message = "Reset the room to initial state to run it again";
    replace_help_message_and_action_fields(help_message, "", action_obj);
  }
  if (event_action == "Start Video Brief"){
    var help_message = "Start the video brief for the room";
    replace_help_message_and_action_fields(help_message, "", action_obj);
  }
  if (event_action == "Start Soundtrack"){
    var help_message = "Start the soundtrack for the room";
    replace_help_message_and_action_fields(help_message, "", action_obj);
  }
  if (event_action == "Stop Soundtrack"){
    var help_message = "Stop the soundtrack for the room";
    replace_help_message_and_action_fields(help_message, "", action_obj);
  }
  if (event_action == "Request Clue from GM"){
    var help_message = "Request a clue from the Game Master through a notification on the GM console";
    replace_help_message_and_action_fields(help_message, "", action_obj);
  }
  if (event_action == "Run Script"){
    action_run_script_request(action_obj);
  }
}

// Function for Event
function event_time_elapsed(this_obj){
  var help_message = "When the running timer has elapsed past the specified min and sec, the attached actions will fire"
  var item = _.template($("#automation-time-elapsed-tpl").html() );
  replace_help_message_and_event_fields(help_message, item);
}

function event_network_polling(){
  var help_message = "When a prop returns a specified value, the attached actions will fire"
  var item = _.template($("#automation-network-polling-tpl").html() );
  replace_help_message_and_event_fields(help_message, item);
}

function event_custom_button(){
  var help_message = "Add a button to the GM console that triggers actions";
  var item = _.template($("#automation-custom-button-tpl").html());
  replace_help_message_and_event_fields(help_message, item);
}

function event_event_name(){
  var help_message = "Listen for a custom JS event triggered by a custom script";
  var item = _.template($("#automation-custom-event-tpl").html() );
  replace_help_message_and_event_fields(help_message, item);
}

function replace_help_message_and_event_fields(help_message, item){
  $(".event-box-body").html(item);
  $(".event-help-message").html(help_message);
}

// Function for action
function action_send_clue_text(this_obj){
  var help_message = "Display this text to the players";
  var item = _.template($("#automation-send-clue-text-tpl").html() );
  replace_help_message_and_action_fields(help_message, item, this_obj);
}

function action_play_sound(this_obj){
  var help_message = "Play uploaded room sound";
  var item = _.template($("#automation-play-sound-tpl").html() );
  replace_help_message_and_action_fields(help_message, item, this_obj);
}

function action_play_video(this_obj){
  var help_message = "Play uploaded room video";
  var item = _.template($("#automation-play-video-tpl").html() );
  replace_help_message_and_action_fields(help_message, item, this_obj);
}

function action_display_images(this_obj){
  var help_message = "Show an image clue";
  var item = _.template($("#automation-display-image-tpl").html() );
  replace_help_message_and_action_fields(help_message, item, this_obj);
}

function action_send_network_request(this_obj){
  var help_message = "Send a network request to a prop";
  var item = _.template($("#automation-send-network-request-tpl").html() );
  replace_help_message_and_action_fields(help_message, item, this_obj);
}

function action_complete_puzzle_request(this_obj){
  var help_message = "Mark selected puzzle complete on the puzzle checklist";
  var item = _.template($("#automation-complete-puzzle-tpl").html() );
  replace_help_message_and_action_fields(help_message, item, this_obj);
}

function action_philips_hue_lights_group_and_scene_request(this_obj){
  var help_message = "Trigger a scene change with the Philips Huge lights";
  var item = _.template($("#automation-ph-lights-group-and-scene-tpl").html() );
  replace_help_message_and_action_fields(help_message, item, this_obj);
}

function action_philips_hue_lights_blink_request(this_obj){
  var help_message = "Blink a group of Philips Huge lights";
  var item = _.template($("#automation-ph-lights-blink-tpl").html() );
  replace_help_message_and_action_fields(help_message, item, this_obj);
}

function action_philips_hue_lights_on_or_off_request(this_obj){
  var help_message = "On/off a group of Philips Huge lights";
  var item = _.template($("#automation-ph-lights-onoff-tpl").html() );
  replace_help_message_and_action_fields(help_message, item, this_obj);
}

function action_adjust_time_request(this_obj){
  var help_message = "Add/subtract minuets from the time remaining (- vals subtract)";
  var item = _.template($("#automation-adjust-time-tpl").html() );
  replace_help_message_and_action_fields(help_message, item, this_obj);
}

function action_run_script_request(this_obj){
  var help_message = "Execute custom Javascript in the GM console";
  var item = _.template($("#automation-run-script-tpl").html() );
  replace_help_message_and_action_fields(help_message, item, this_obj);
}

function replace_help_message_and_action_fields(help_message, item, this_obj){
  this_obj.parents(".page_form").find(".action-inner-box-body").html(item);
  this_obj.parents(".page_form").find(".action-help-message").html(help_message);
}

function get_event_form_fields(el_event){
  var event_dict = {}
  event_dict['event_id'] = el_event.find('select[name="event_type"]').val();
  event_dict['event_sec'] = el_event.find('input[name="event_sec"]').val();
  event_dict['event_min'] = el_event.find('input[name="event_min"]').val();
  event_dict['url'] = el_event.find('input[name="url"]').val();
  event_dict['trigger_value'] = el_event.find('input[name="trigger_value"]').val();
  event_dict['poll_interval'] = el_event.find('input[name="poll_interval"]').val();
  event_dict['button_label'] = el_event.find('input[name="button_label"]').val();
  event_dict['trigger_event_name'] = el_event.find('input[name="trigger_event_name"]').val();
  return event_dict
  // var event_type_val = (event_type != "") ? event_dict['event_type']= event_type : "";
  // var event_max_val = (event_type != "") ? event_dict['event_max']= event_max : "";
  // var event_min_val = (event_type != "") ? event_dict['event_min']= event_min : "";
  // var url_val = (event_type != "") ? event_dict['url']= url : "";
  // var trigger_val = (event_type != "") ? event_dict['trigger_value']= trigger_value : "";
  // var poll_interval_val = (event_type != "") ? event_dict['poll_interval']= poll_interval : "";
  // var button_label_val = (event_type != "") ? event_dict['button_label']= button_label : "";
  // var trigger_event_val = (event_type != "") ? event_dict['trigger_event_name']= trigger_event_name : "";
}

function get_action_form_fields(el_action){
  action_list= []
  el_action.find(".page_form").each(function() {
    var action_dict = {}
    action_dict['action_id'] = $(this).find('select[name="event_action"]').val();
    action_dict['clue_text'] = $(this).find('input[name="clue_text"]').val();
    action_dict['sound_id'] = $(this).find('select[name="sound"]').val();
    action_dict['video_id'] = $(this).find('select[name="video"]').val();
    action_dict['room_images_id'] = $(this).find('select[name="room_images"]').val();
    action_dict['url'] = $(this).find('input[name="url"]').val();
    action_dict['puzzle_id'] = $(this).find('select[name="puzzle"]').val();
    action_dict['time_to_adjust'] = $(this).find('input[name="time_to_adjust"]').val();
    action_dict['script_name'] = $(this).find('input[name="script_name"]').val();
    action_dict['script_text'] = $(this).find('textarea[name="script_text"]').val();
    action_dict['blink_interval'] = $(this).find('input[name="blink_interval"]').val();
    action_dict['duration'] = $(this).find('input[name="duration"]').val();
    action_dict['group_id'] = $(this).find('select[name="group_id"]').val();
    action_dict['scene_id'] = $(this).find('select[name="scene_id"]').val();
    action_dict['light_state'] = $(this).find('select[name="light_state"]').val();

    // eval(JSON.stringify($(this).find('textarea[name="script_text"]').val()));
    action_list.push(action_dict);
  });
  return action_list
}


function all_type_event_actions () {
  var collection_all_fields = {};
  $(".grey_box").each(function() {
    if ($(this).find(".action-box-body").length > 0){
      collection_all_fields['action_fields'] = get_action_form_fields($(this));
    }else{
      collection_all_fields['event_fields'] = get_event_form_fields($(this));
    }
  });
  return collection_all_fields
};

$(".automation_submit").click(function(){
    var questions = all_type_event_actions();
    var data_json = JSON.stringify(questions);
    $("#create-automation-form").find('input[name="data_json"]').val(data_json);
    $("#create-automation-form").submit()
});

$(document).on('click', '#test-script', function(){
  $(".execute-message").show();
  try{
    eval($("#id_script_text").val());
    $("#error_script_text").hide();
    $("#success_script_text").text("Script ran without error");
  }catch (e) {
    $("#success_script_text").hide();
    $("#error_script_text").text("Error running script (see JS console)");
    console.error(e);
  }
});

$(document).on('click', '#test-connection', function(){
  var url = $("#id_url").val(),
      test_url_room_id = url.split("/")[5];
  if (room_id != test_url_room_id){
    connection_fails("error");
    $("#connection-response").hide();
    return;
  }

  $.ajax({
    type: "GET",
    url:url,
    success:function(e){
      if(e.roomId == room_id){
        connection_success(e);
      }else{
        connection_fails("error");
      }
    },
    error:function(e,n,o){
      connection_fails(e.statusText)
    },
    complete:function(){
      more_or_less_content();
      $("#connection-response").addClass("text-dark");
      $("#connection-status").show();
      ;
    },
  });
});

function connection_success(response) {
  $("#connection-status").removeClass("text-danger");
  $("#connection-status").addClass("text-success");
  $("#connection-status").text("Connection Succeeded!");
  $("#connection-response").text("Response: "+JSON.stringify(response));
  $("#connection-response").show();
}

function connection_fails(status) {
  $("#connection-response").show();
  $("#connection-status").removeClass("text-success");
  $("#connection-status").addClass("text-danger");
  $("#connection-status").text("Connection Failed!");
  if (status != "error"){
    $("#connection-response").text("Response: "+status);
  }else{
    $("#connection-response").hide();
  }
}

function more_or_less_content(){
  var showChar = 291;
  var ellipsestext = "...";
  var moretext = "more";
  var lesstext = "less";
  $('.more').each(function() {
    var content = $(this).html();

    if(content.length > showChar) {

      var c = content.substr(0, showChar);
      var h = content.substr(showChar-1, content.length - showChar);

      var html = c + '<span class="moreelipses">'+ellipsestext+'</span><span class="morecontent"><span>' + h + '</span><a href="" class="morelink text-primary">'+moretext+'</a></span>';

      $(this).html(html);
    }

  });

  $(".morelink").click(function(){
    if($(this).hasClass("less")) {
      $(this).removeClass("less");
      $(this).html(moretext);
    } else {
      $(this).addClass("less");
      $(this).html(lesstext);
    }
    $(this).parent().prev().toggle();
    $(this).prev().toggle();
    return false;
  });
}
