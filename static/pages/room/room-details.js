var winRef; //This holds the reference to your page, to see later it is open or not
var winLiveCounter;
var action_btn_name = "";
var clue_textarea_value;
var currentVideoClue;
var currentAudioClue;
var videoBrief;
var videoBriefContainer;
var videoClueObject;
var bgvidObject;
var roomCompleted = false;
var showOverlay = false;
var gmCounter = $('#countdown');
var csrftoken = getCookie('csrftoken');
var isReuqestClueSent = false;
// var soundtrack_value = 24;
// var alert_tone_value = 24;
// var end_sound_track_value = 24;
// var voice_transmission_value = 24;
// var audio_clue_value = 24;
// var video_brief_value = 24;
// var background_video_value = 24;
// var video_value = 24;
var istimeElapse = true;
var timeElapseList = [];
var defaultTimeMin = parseInt(default_time_limit);
var displayTimeMs = isCheckBoolean(display_timer_milliseconds);
var timer_obj = new Timer(defaultTimeMin, displayTimeMs, 1);
var is_nwk_fire = false;
timer_obj.addStartTimerCb(startTimer);
timer_obj.addStopTimerCb(stopTimer);
timer_obj.addTimeUpdatedCb(updateTimer);
timer_obj.addTimeUpCb(upTime);


$('#cd_start2').on('click', startOrStopTimer);

// $(document).on('click', ".open-live-view-popup", function (event) {
//   event.preventDefault();
//   var popup_type = $(this).val();
//   var cd_seconds = parseInt($("#cd_seconds").val());
//   if(isLiveWindowOpen()){
//     var run_room_name = $("#id_run_room_name").text();
//     $(".close").click();
//   }else{
//     $("#pleaseOpenLiveView .modal-body").html("<p class='btn-start'>Please open the Live View Window.</p>");
//     $("#pleaseOpenLiveView .modal-title").html("<p class='btn-start'>Communication Error</p>");
//     $("#pleaseOpenLiveView .modal-body").parent().find("#id-open-live-window").show();
//     $("#pleaseOpenLiveView").modal({
//       backdrop: 'static'
//     });
//   }
// });

$(document).on('click', "#id-open-live-window", function (event) {
  openLiveWindow($(this).data("room-id"));
});

$(document).on('click', "#open-live-window-id", function (event) {
  if(!isLiveWindowOpen()){
    openLiveWindow($(this).data("room-id"));
  }else{
    $("#gmLiveViewAlreadyOpen").modal({
      backdrop: 'static'
    });
  }
});

$(".wan-spinner-2").WanSpinner().css("border-color", "#2C3E50");

$(".page_left_panel").addClass("newpage_left_panel_hide");
$(".page_right_panel").addClass("newpage_right_panel_hide");

$(".menu_toogle a").click(function(){
  $(".page_left_panel").toggleClass('newpage_left_panel_hide');
  $(".page_left_panel").removeClass('page_left_panel_hide');
  $(".page_right_panel").removeClass('page_right_panel_hide');
  $(".page_right_panel").toggleClass('newpage_right_panel_hide');
});

$('#btn-update-time').unbind().bind('click', function(){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  alterTime(parseInt(document.getElementById('id-update-min').value));
});

$("#gameMasterClueInput").bind("keypress", function(event) {
  if(event.which == 13 && !event.shiftKey) {
    if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
    event.preventDefault();
    updateClueArea();
  }
});

$('#gmUpdateText').unbind().bind('click', function(){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  updateClueArea();
});

$('#id-full-screen').on("click", function() {
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  if (winRef.outerWidth < screen.availWidth || winRef.outerHeight < screen.availHeight)
  {
    winRef.moveTo(0,0);
    winRef.resizeTo(screen.availWidth, screen.availHeight);
    winRef.focus();
  }
});

$("#saveAndSendLiveText").click(function(){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  var send_text = document.getElementById('gmLivePreviewText').innerHTML;
  if(send_text.length > 0){
    saveLiveText(send_text);
  }
});

$("#noSaveText").click(function(){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  var message_dialog = $("#message-dialog");
  message_dialog.find('p strong').html('No permission for clue text save');
  message_dialog.show();
  $(window).scrollTop($('#message-dialog').offset().top);
  message_dialog.fadeOut(10000);
});

$("#gmBtnClearLiveText").click(function(){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  clearLiveText();
});

$("#gmBtnCloseLiveView").click(function(){
  if(!isLiveWindowOpen()){
    $("#liveViewAlreadyClosed").modal({
      backdrop: 'static'
    });
    return;
  }
  else{
    $("#gmConfirmCloseLiveView").modal({
      backdrop: 'static'
    });
  }
});

$("#id-reset-room-popup").click(function(){
  resetRoom();
});

$("#gm-reset-room").on('click', function(){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
    $("#gmResetRoom").modal({
      backdrop: 'static'
    });
    return false;
});

$("#gm-puzzles-popup").on('click', function(){
  if(isLiveWindowOpen()){
    $("#puzzles-modal").modal({
      backdrop: 'static'
    });
    return false;
  }
});

$("#spin").hide();

$("#gmAlertButton").click(function(){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  winRef.alertToneSound.play();
});

$("#videoBriefBtn").click(function(){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  if($(this).data("src").length < 1){
    $("#uploadVideoBriefWarning").modal({
      backdrop: 'static'
    });
    return false;
  }else{
    winRef.$(".showfullscreen").hide();
    playPauseVideo();
  }
});

$(".playVideos").click(function(){
  var videoID = $(this).attr("id");
  if(isLiveWindowOpen()){
    winRef.$(".showfullscreen").hide();
    playPauseVideoClue(videoID);
  }
});

$("#predefinedClues").click(function (event) {
  if(isLiveWindowOpen()){
    var clue = $(event.target)[0];
    document.getElementById('gameMasterClueInput').value = clue.text;
  }
});

$('.clueImage').on("click", function(clickedImage) {
  if(isLiveWindowOpen()){
    winRef.$(".showfullscreen").hide();
    displayImageClue(clickedImage.currentTarget.currentSrc);
  }
});

$(".playSound").click(function(){
  var audioID = $(this).attr("id");
  playPauseAudioClue(audioID)
  audioClue(audioID);
});

$("#soundtrackReset").click(function(){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  resetSoundtrack();
});

$("#completeRoom").click(function(){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  completeRoom();
  return false;
});

$("#soundtrackSlider").slider({
  value : (localStorage.getItem('stSlider'+room_id) || 75),
  step  : 1,
  range : 'min',
  min   : 0,
  max   : 100
}).on("slidechange", function( event, ui ) {
  var value = $("#soundtrackSlider").slider("value");
  localStorage.setItem('stSlider'+room_id, value);
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  if (! winRef.soundtrackAudio) return;

  if(value < 5){
    winRef.soundtrackAudio.volume = 0;
  }else{
    winRef.soundtrackAudio.volume = (value / 100);
  }
});

$("#alertToneSlider").slider({
  value : (localStorage.getItem('atSlider'+room_id) || 75),
  step  : 1,
  range : 'min',
  min   : 0,
  max   : 100
}).on("slidechange", function( event, ui ) {
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  var value = $("#alertToneSlider").slider("value");
  localStorage.setItem('atSlider'+room_id, value);
  alert_tone_value = value;
  if (! winRef.alertToneSound) return;
  if(value < 5){
    winRef.alertToneSound.volume = 0;
  }else{
    winRef.alertToneSound.volume = (value / 100);
  }
});

$("#roomEndSoundtrackSlider").slider({
  value : (localStorage.getItem('reSlider'+room_id) || 75),
  step  : 1,
  range : 'min',
  min   : 0,
  max   : 100
}).on("slidechange", function( event, ui ) {
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  var value = $("#roomEndSoundtrackSlider").slider("value");
  localStorage.setItem('reSlider'+room_id, value);
  if (! winRef.successsoundTrack) return;

  if(value < 5){
    if (winRef.successsoundTrack) winRef.successsoundTrack.volume = 0;
    if (winRef.failedSoundTrack) winRef.failedSoundTrack.volume = 0;
  }else{
    if (winRef.successsoundTrack) winRef.successsoundTrack.volume = (value / 100);
    if (winRef.failedSoundTrack) winRef.failedSoundTrack.volume = (value / 100);
  }
});

$("#voiceTransmissionSlider").slider({
  value : (localStorage.getItem('vtSlider'+room_id) || 75),
  step  : 1,
  range : 'min',
  min   : 0,
  max   : 100
}).on("slidechange", function( event, ui ) {
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  var value = $("#voiceTransmissionSlider").slider("value");
  localStorage.setItem('vtSlider'+room_id, value);
  if (! winRef.microphone) return;
  winRef.microphone.volume = (value / 100);
});

$("#videoBriefSlider").slider({
  value : (localStorage.getItem('vbSlider'+room_id) || 75),
  step  : 1,
  range : 'min',
  min   : 0,
  max   : 100
}).on("slidechange", function( event, ui ) {
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  var value = $("#videoBriefSlider").slider("value");
  localStorage.setItem('vbSlider'+room_id, value);
  if(videoBrief != undefined && videoBrief != null){
    if(value < 1){
      videoBrief.volume = 0;
    }else{
      videoBrief.volume = (value / 100);
    }
  }
});

$("#backgroundVideoSlider").slider({
  value : (localStorage.getItem('bvSlider'+room_id) || 75),
  step  : 1,
  range : 'min',
  min   : 0,
  max   : 100
}).on("slidechange", function( event, ui ) {
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  var value = $("#backgroundVideoSlider").slider("value");
  localStorage.setItem('bvSlider'+room_id, value);
  if(winRef.videoBackground != undefined && winRef.videoBackground != null){
      if(value < 1){
        winRef.videoBackground.volume = 0;
      }else{
        winRef.videoBackground.volume = (value / 100);
      }
  }
});

$("#videoSlider").slider({
  value : (localStorage.getItem('vcSlider'+room_id) || 75),
  step  : 1,
  range : 'min',
  min   : 0,
  max   : 100
}).on("slidechange", function( event, ui ) {
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  var value = $("#videoSlider").slider("value");
  localStorage.setItem('vcSlider'+room_id, value);

  if(winRef.videoClueObject){
    if(value < 1){
      winRef.videoClueObject.volume = 0;
    }else{
      winRef.videoClueObject.volume = (value / 100);
    }
  }
});

$("#liveAudioButton").click(function(){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  transmitAudioOnOff($(this));
});

$("#overlay").click(function(){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  if(!winRef.cachedOverlayImage) {
    $("#overlayImageWarning").modal({
      backdrop: 'static'
    });
    return false;
  }else{
    hideShowOverlay();
  }
});

$('#soundtrackRepeat').change(function() {
  if(!isLiveWindowOpen()){
    $('#pleaseOpenLiveView').modal();
    this.checked = ! this.checked;
    return false;
  }

  if (winRef.soundtrackAudio)
    winRef.soundtrackAudio.loop = this.checked;
});

$("#puzzle-list-table .chk-puzzle").click(function(){
  puzzleComplete($(this));
});

$("input:radio[name=speedOptions]").on('change', function() {
  changeSpeed($(this).val());
});

$(window).bind('unload', function() {
  if (winRef)
    winRef.close();
});

$(".customButton").click(function(){
  customButtomAction($(this));
});

/*$("#saveleaderboards").click(function(){
  $("#puzzleprint").parent().show();
});*/

$("#puzzleprint").click(function(){
  window.open($(this).attr("href"), 'puzzles');
});

// Js writtern on puzzle edit in popup

$('#gm-puzzles-popup').on('click',function(){
  $('.puzzle_td').hide();
  $('.puzzle_click').hide();
});

$('.onClickEditPuzzle').click(function(){
  var click_id = $(this)[0].dataset.id;
  var click_key = $(this)[0].dataset.key;
  var name_id = ".puzzle_name_check_" + click_id;
  var notes_id = ".puzzle_notes_check_"+ click_id;
  var input_name =".puzzle_name_input_" + click_id;
  var input_note = ".puzzle_notes_input_"+ click_id;
  $(name_id).hide();
  $(notes_id).hide();
  $(input_name).show();
  $(input_note).show();
  $('.puzzle_edit_' + click_id).hide();
  $('.puzzle_save_' + click_id).show();
  });

$('.onClicksavePuzzle').click(function(){
  var click_id = $(this)[0].dataset.id;
  var click_key = $(this)[0].dataset.key;
  var room_id = $(this)[0].dataset.room;
  var instructions = $(this)[0].dataset.instructions;

  var name_id = ".puzzle_name_check_" + click_id;
  var notes_id = ".puzzle_notes_check_"+ click_id;
  var input_name =".puzzle_name_input_" + click_id;
  var input_note = ".puzzle_notes_input_"+ click_id;

  var puzzle_name = $(input_name).children()[0].value;
  var damage_or_notes = $(input_note).children()[0].value;
  // var csrftoken = getCookie('csrftoken');

  var puzzle_url= URLS.update_room_puzzle.replace('99999999',room_id).replace('88888888',click_id);
  $.ajax({
    url: puzzle_url,
    type: "POST",
    data:{'puzzle_name':puzzle_name,'damage_or_notes':damage_or_notes,'reset_instructions':instructions,"csrfmiddlewaretoken":csrftoken},
    success: function(response) {
      if(response.messages == "Successfully updated"){
        $(name_id).text(puzzle_name);
        $(notes_id).text(damage_or_notes);
      }else{
        alert(response.messages);
      }
      $(name_id).show();
      $(notes_id).show();
      $(input_name).hide();
      $(input_note).hide();
      $('.puzzle_edit_' + click_id).show();
      $('.puzzle_save_' + click_id).hide();
    }
  });
});

function isCheckBoolean(val){
  return (val == "True" ? true : false);
}

function startTimer() {
  console.log('timer started');
  winLiveCounter = winRef.$('#countdown');

  if (winRef && winRef.videoBackground) winRef.videoBackground.play();

  console.log('Timer started');
  var cusStartEvent = isEventExitsOrNot("timerStarted");
  customAutomationEvent("timerStarted", cusStartEvent);
  if (roomCompleted) {
    console.log("Can't start timer when room is completed!");
    return;
  }

  if(isCheckBoolean(play_soundtrack_on_timer_start) && winRef && winRef.soundtrackAudio && winRef.soundtrackAudio.paused) {
    checkPlayAndPause();
  }

  hideOverlay();
  if (isCheckBoolean(start_background_video_on_timer_start)) winRef.videoBackground.play();

  $('#cd_start2').val("Pause");
}

function stopTimer() {
  console.log('timer stopped');
  var cusStopEvent = isEventExitsOrNot("timerStopped");
  customAutomationEvent("timerStopped", cusStopEvent);
  if (winRef && winRef.videoBackground) winRef.videoBackground.pause();
  $('#cd_start2').val("Start");
}

function timeConvertToSecond(){
  var currentTime = winLiveCounter.text().split(":");
  var curMin = parseInt(currentTime[0]);
  var curSec = parseInt(currentTime[1].split(".")[0]);
  var totalSeconds = ((curMin * 60) + curSec) * 100;
  $("#id-start-time").val(totalSeconds);
}

function updateTimer() {
  var s = timer_obj.displayStr();
  if (winLiveCounter != undefined){
    timeConvertToSecond()
    cusTimeElapsed = isEventExitsOrNot("timeElapsed");
    customAutomationEvent("timeElapsed", cusTimeElapsed);
  }

  gmCounter.text(s);
  if (winLiveCounter) {
    winLiveCounter.text(s);
  } else if (winRef) {
    winLiveCounter = winRef.$('#countdown');
    winLiveCounter.text(s);
  }
}

function upTime() {
  console.log('out of time');
  failRoom();
}

updateTimer();

function startOrStopTimer() {
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}

  if (roomCompleted) {
    console.log("We can not start timer when room is completed!");
    return;
  }

  if (timer_obj.timeRemaining == 0) {
      alert('Room has completed, please reset the room!');
      return false;
  }
  hideOverlay();

  timer_obj.toggle();
}

function playAlertTone() {
  winRef.alertToneSound.play();
}
function updateClueArea() {
  if(isLiveWindowOpen()){
    var replacementText = $('#gameMasterClueInput').val();
    $('#gameMasterClueInput').val("");
    sendClueText(replacementText);
  }
}

function sendClueText(msg) {
  winRef.document.getElementById('communicationText').innerHTML = msg;
  document.getElementById('gmLivePreviewText').innerHTML = msg;
  if(isCheckBoolean(audio_alert_on_clue_send)) {playAlertTone();}
}

updateClueStatusEvtHandler('.gm-clue-off', '.gm-clue-on');
updateClueStatusEvtHandler('.gm-clue-on', '.gm-clue-used');
updateClueStatusEvtHandler('.gm-clue-used', '.gm-clue-off');

var options = {
  maxValue: 10,
  minValue: -5,
  step: 0.131,
  inputWidth: 100,
  start: -2,
  plusClick: function(val) {
    console.log(val);
  },
  minusClick: function(val) {
    console.log(val);
  },
  exceptionFun: function(val) {
    console.log("excep: " + val);
  },
  valueChanged: function(val) {
    console.log('change: ' + val);
  }
}

function updateClueStatusEvtHandler(currClass, nextClass) {
  $(currClass).click(function (event) {
    if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
    var lock_type = currClass.split("-")[2];
    var lock_number = $(this).attr("data-lock-id");
    if(isCheckBoolean(audio_alert_on_clue_count_change)) {playAlertTone();}
    var $this = $("#fa-"+lock_type+"-"+lock_number+"").closest(currClass);
    var $next = $this.closest('.gm-clue-element').find(nextClass);
    $this.hide();
    $next.show();
    updateLiveViewClueDisplay();
  });
}

function openLiveWindow(roomId) {
    if(isLiveWindowOpen()){$('#liveViewAlreadyOpen').modal();return;}
    $('#loadingAssets').modal({backdrop: 'static', keyboard: false});
    var liveWindowParams = 'width=' + (screen.width - 200);
    liveWindowParams += ', height=' + (screen.height - 200);
    liveWindowParams += ', left=1000';
    liveWindowParams += ', menubar=1';

    $(".close").click();
    // var room_id = this_obj.dataset.roomId;
    var url = URLS.dashboard_new_live_view_details.replace("11111111", roomId);
    if (typeof (winRef) == 'undefined' || winRef.closed) {
        //create new, since none is open
        winRef = window.open(url,'Open Live View','width=1170px,height=570px', liveWindowParams);
    }
    else {
        try {
          winRef.document; //if this throws an exception then we have no access to the child window - probably domain change so we open a new window
        }
        catch (e) {
            winRef = window.open(url,'Open Live View','width=1170px,height=570px',liveWindowParams);
        }

        //IE doesn't allow focus, so I close it and open a new one
        if (navigator.appName == 'Microsoft Internet Explorer') {
            winRef.close();
            winRef = window.open(url,'Open Live View','width=1170px,height=570px', liveWindowParams);
        }
        else {
            //give it focus for a better user experience
            winRef.focus();
        }
    }

    winRef.onbeforeunload = function (e) {
      winRef = null;
      $('#overlay').text('Show Overlay');
      showOverlay = false;
    };

    winRef.window.onload = function() {
      winRef.$('#countdown').text($('#countdown').text());
      hideShowOverlay();
      // if(background_video){
      //   winRef.$('#bodyMainContainerDiv').hide();
      //   winRef.$('#bgImageContainer').hide();
      // }

    };
    // hideShowOverlay();

    if (window.focus) {winRef.focus()}
}

function isLiveWindowOpen() {
  return !!(winRef && ! winRef.closed)
}

window.onbeforeunload = function() {
  // winRef.close();
  return "Data will be lost if you leave the page, are you sure?";
};

function set_winRef(){
  winRef = undefined;
}

// Common functions
function pad(number, length) {
    var str = '' + number;
    while (str.length < length) {str = '0' + str;}
    return str;
}

function formatTime(time) {
  var min = parseInt(time / 6000),
    sec = parseInt(time / 100) - (min * 60),
    hundredths = pad(time - (sec * 100) - (min * 6000), 2);
  if (isCheckBoolean(display_timer_milliseconds)){
    return (min > 0 ? pad(min, 2) : "00") + ":" + pad(sec, 2) + "." + hundredths;
  }  else{
    return (min > 0 ? pad(min, 2) : "00") + ":" + pad(sec, 2);
  }
}

function saveLiveText(send_text){
  $("#spin").show();
  $.ajax({
      type: "POST",
      url: URLS.room_clue_create,
      data: {"name":send_text,
             "csrfmiddlewaretoken":csrftoken, "room": room_id},
      dataType: "json",
      success: function(response){
        var clue_name = response.clue_name;
        var option_html = '<li><a href="#" role="button" class="open-live-view-popup btn_add_or_remove_popup">'+clue_name+'</a></li>';
        $("#predefinedClues").append(option_html);
        $("#spin").hide();
        var message_dialog = $("#message-dialog");
        message_dialog.find('p strong').html('Clue successfully saved!!');
        message_dialog.show();
        $(window).scrollTop($('#message-dialog').offset().top);
        message_dialog.fadeOut(10000);
      }
  });
}

function clearLiveText() {
  if(isLiveWindowOpen()){
    $(winRef.document).find('#communicationText').text("");
    $(document).find('#gmLivePreviewText').text("");
    winRef.document.getElementById('photoClueContainer').style.display = 'none';
  }
}

function closeLiveView(){
  $(".close").click();
  winRef.close();
  winRef = null;
}

function checkPlayAndPause(){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  if (! winRef.soundtrackAudio) {
    $('#uploadSoundTrackWarning').modal();
    return ;
  }

  try{
    // if (winRef.soundtrackAudio == undefined) return;
    if (winRef.soundtrackAudio.paused){
      playSoundtrack();
    }else{
      pauseSoundtrack();
    }
  }catch (e) {
    // $("#id_custom_header_includes").after("<div class='script_val' style='color:red;'>Error running script (see JS console)</div>");
    alert("Soundtrack file is not found!!!")
    console.error(e);
  }
}

function playSoundtrack() {
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  // if (winRef.soundtrackAudio == undefined) return;
  try{
    winRef.soundtrackAudio.loop = $('#soundtrackRepeat').prop('checked');
    winRef.soundtrackAudio.play();
  }catch (e) {
    // $("#id_custom_header_includes").after("<div class='script_val' style='color:red;'>Error running script (see JS console)</div>");
    alert("Soundtrack file is not found!!!")
    console.error(e);
  }

  var playandpause = document.getElementById('gmplayandpause');
  playandpause.innerHTML = '<i class="fa fa-pause-circle" aria-hidden="true"></i>';
  winRef.soundtrackAudio.onended = function(e) {
    winRef.soundtrackAudio.currentTime = 0;
  };
}

function pauseSoundtrack() {
  if (! winRef || ! winRef.soundtrackAudio) {
    return;
  }
  var playandpausebtn = document.getElementById('gmplayandpause');
  winRef.soundtrackAudio.pause();
  playandpausebtn.innerHTML = '<i class="fa fa-play-circle" aria-hidden="true"></i>';
}

function playPauseVideo() {
  videoBrief = winRef.document.getElementById("videoBriefObject");
  videoBriefContainer = winRef.document.getElementById("videoBriefContainer");
  var videoBriefSource = winRef.document.getElementById("vidSrc").getAttribute('src');

  if(winRef.videoBackground) winRef.document.getElementById('bgvidObject').style.display='none';

  if(videoBriefSource == "" || videoBriefSource == null){$('#uploadVideoBriefWarning').modal();return;}

  videoBrief.volume = $("#videoBriefSlider").slider("value")/100;

  if (videoBrief.paused){
    //show container
    videoBriefContainer.style.display = 'block';
    videoBrief.load();
    videoBrief.play();
    if(winRef.videoBackground) document.getElementById('videoBriefBtn').innerHTML = 'Hide Video Brief<span><i class="fa fa-pause" aria-hidden="true"></i></span>';
    winRef.$('#bodyMainContainerDiv').hide();
    winRef.$('#bgImageContainer').hide();
  }else{
    //hide container
    winRef.$('#bodyMainContainerDiv').show();
    winRef.$('#bgImageContainer').show();
    videoBrief.pause();
    videoBrief.currentTime = 0;
    videoBriefContainer.style.display = 'none';
    if(winRef.videoBackground) winRef.document.getElementById('bgvidObject').style.display='block';
    document.getElementById('videoBriefBtn').innerHTML = 'Show Video Brief<span><i class="fa fa-play" aria-hidden="true"></i></span>';
  }

  videoBrief.onended = function(e){
    videoBrief.currentTime = 0;
    videoBriefContainer.style.display = 'none';
    document.getElementById('videoBriefBtn').innerHTML = 'Show Video Brief<span><i class="fa fa-play" aria-hidden="true"></i></span>';
    winRef.$('#bodyMainContainerDiv').show();
    if(winRef.videoBackground) winRef.document.getElementById('bgvidObject').style.display='block';

    if(isCheckBoolean(start_timer_after_video_brief)) {$('#cd_start2').click();}

    if(winRef.videoBackground) winRef.videoBackground.play();
    winRef.$('#bodyMainContainerDiv').show();
    winRef.$('#bgImageContainer').show();
  };
}

function playPauseVideoClue(videoID) {
  videoClueContainer = winRef.document.getElementById("videoClueContainer");
  videoClueObject = winRef.document.getElementById("videoClueObject");
  var videoClueSrc = winRef.document.getElementById("vidClueSrc");

  var cluebtn = document.getElementById(videoID);
  if(winRef.videoBackground) winRef.document.getElementById('bgvidObject').style.display='none';

  if (! cluebtn) return;

  if(videoClueObject.paused || currentVideoClue != videoID) {
      if(currentVideoClue) {
        document.getElementById(currentVideoClue).className = 'btn btn-success glyphicon glyphicon-play';
      }
      videoClueContainer.style.display = 'block';
      videoClueObject.src = winRef["clueVideo"+videoID];
      videoClueObject.load();
      videoClueObject.play();
      cluebtn.className = 'btn btn-success glyphicon glyphicon-stop';
      winRef.$('#bodyMainContainerDiv').hide();
      winRef.$('#bgImageContainer').hide();
  } else {
    videoClueObject.pause();
    videoClueContainer.style.display = 'none';
    cluebtn.className = 'btn btn-success glyphicon glyphicon-play';
    currentVideoClue = '';
    winRef.$('#bodyMainContainerDiv').show();
    winRef.$('#bgImageContainer').show();
  }
  videoClueObject.onended = function(e){
    videoClueObject.currentTime = 0;
    videoClueContainer.style.display = 'none';
    cluebtn.className = 'btn btn-success glyphicon glyphicon-play';
    if(winRef.videoBackground) winRef.document.getElementById('bgvidObject').style.display='block';
    winRef.$('#bgImageContainer').show();
    winRef.$('#bodyMainContainerDiv').show();
  };
  currentVideoClue = videoID;
}

function resetVideoClue() {
  console.log('Resetting Video Clues');
  if(currentVideoClue) {
    var cluebtn = document.getElementById(currentVideoClue);
    videoClueObject.pause();
    videoClueContainer.style.display = 'none';
    cluebtn.className = 'btn btn-success glyphicon glyphicon-play';
    currentVideoClue = '';
  }
}

function displayImageClue(url) {
  winRef.document.getElementById('photoClueContainer').style.display = 'block';
  winRef.document.getElementById('photoClueOutput').src = url;
  winRef.$('#bodyMainContainerDiv').hide();
  if(isCheckBoolean(audio_alert_on_image_clue_send)) {playAlertTone();}
  $(document).find('#gmLivePreviewText').text("Image is currently live.");
}


function playPauseAudioClue(audioID){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  var playPauseButton = document.getElementById(audioID);

  if (! winRef["clueAudio"+audioID]) return;

  if (winRef["clueAudio"+audioID].paused){
      winRef["clueAudio"+audioID].play();
      playPauseButton.className = 'btn btn-success playSound glyphicon glyphicon-stop';
  }else{
      //hide container
      winRef["clueAudio"+audioID].pause();
      playPauseButton.className = 'btn btn-success playSound glyphicon glyphicon-play';
  }

  winRef["clueAudio"+audioID].onended = function(e) {
      winRef["clueAudio"+audioID].currentTime = 0;
      playPauseButton.className = 'btn btn-success playSound glyphicon glyphicon-play';
  };
}

function resetRoom() {
  timer_obj.stop();
  timer_obj.reset();
  changeSpeed(1);
  $("input:radio[name=speedOptions][disabled=false]:first").attr('checked', true);
  $('div#speedSelect label:eq(0)').addClass('active');
  $('div#speedSelect label:eq(1)').removeClass('active');
  $('div#speedSelect label:eq(2)').removeClass('active');
  //reset clues notification elements
  resetClueCountDisplay();
  //reset data feed
  $('#gameMasterClueInput').val("");
  var awt = initialDataFeedText;
  document.getElementById('gmLivePreviewText').innerHTML = awt;
  winRef.document.getElementById('communicationText').innerHTML = awt;

  //reset soundtrack position
  resetSoundtrack();

  //reset video brief
  if (videoBrief) {
      videoBrief.pause();
      videoBrief.currentTime = 0;
  }
  if (videoBriefContainer) {
    videoBriefContainer.style.display = 'none';
  }

  if(!winRef.cachedOverlayImage) {
    winRef.document.getElementById('photoClueContainer').style.display = 'none';
  }
  // winRef.document.getElementById('bgvidObject').style.display='none';
  winRef.$('#bgvidSrc').parent().hide();
  //reset game ending videos if they exist
  if (winRef.failVideo) resetFailVideo();
  if (winRef.successVideo) resetSuccessVideo();

  //reset video background
  if (winRef.videoBackground) resetBackgroundVideo();
  //reset game ending videos if they exist
  if(!showOverlay){
    hideShowOverlay();
  }

  //only do if the video brief is there, otherwise button will be null
  document.getElementById('videoBriefBtn').innerHTML = 'Show Video Brief<span><i class="fa fa-play" aria-hidden="true"></i></span>';
  //close end of room messages
  $(winRef.document.documentElement).find('.roomEnd').css('display', 'none');

  var cusRoomReset = isEventExitsOrNot("roomReset");
  customAutomationEvent("roomReset", cusRoomReset);

  $(".close").click();
  if (winRef.document.getElementById('bgImageContainer')) winRef.document.getElementById('bgImageContainer').style.display = 'block'; 
  winRef.$('#bodyMainContainerDiv').show();
  // Allow for the room to be "completed"
  roomCompleted = false;
  $("#cd_start2").val("Start");
  winRef.document.getElementById('countdown').textContent = document.getElementById('countdown').innerHTML;
}


function resetBackgroundVideo(){
  if (!winRef.document.getElementById('bgvidObject')) return;
  winRef.document.getElementById('bgvidObject').style.display='block';
  winRef.document.getElementById('bgvidObject').pause();
  winRef.document.getElementById('bgvidObject').currentTime = 0;
}

function resetClueCountDisplay() {
  var $clueIcons = $('.gm-clue-element');
  $clueIcons.children().hide();
  $clueIcons.find('.gm-clue-off').show();
  updateLiveViewClueDisplay();
}

function updateLiveViewClueDisplay() {
  winRef.document.getElementById('liveClueDisplay').innerHTML = document.getElementById('gmClues').innerHTML;
}

function resetSoundtrack(){
  if (winRef.soundtrackAudio) {
    winRef.soundtrackAudio.load();
    winRef.soundtrackAudio.currentTime = 0;
  }
  if (winRef.failedSoundTrack) {
    winRef.failedSoundTrack.load();
    winRef.failedSoundTrack.currentTime = 0
  }
  if (winRef.successsoundTrack) {
    winRef.successsoundTrack.load();
    winRef.successsoundTrack.currentTime = 0;
  }

  $("#gmplayandpause").find("i").addClass("fa-play-circle");
  $("#gmplayandpause").find("i").removeClass("fa-pause-circle");

  $(".playSound").each(function(){
    var resetAudioID = $(this).attr("id");
    winRef["clueAudio"+resetAudioID].load();
    winRef["clueAudio"+resetAudioID].currentTime = 0;
    document.getElementById(resetAudioID).className = 'btn btn-success glyphicon glyphicon-play playSound';
  });
  roomCompleted = false;
}

function resetFailVideo(){
  winRef.failVideo.pause();
  winRef.failVideo.currentTime = 0;
  winRef.failVideo.style.display = 'none';
}
function resetSuccessVideo(){
  winRef.successVideo.pause();
  winRef.successVideo.currentTime = 0;
  winRef.successVideo.style.display = 'none';
}

function completeRoom(){
  if (roomCompleted) {
    console.log("Room is already complete!");
    return;
  }
  var cusRoomCompleted = isEventExitsOrNot("roomCompleted");
  customAutomationEvent("roomCompleted", cusRoomCompleted);
  // winRef.$('#bodyMainContainerDiv').hide();

  resetVideoClue();
  if (!!winRef.document.getElementById('bgImageContainer')) winRef.document.getElementById('bgImageContainer').style.display = 'none';
  if (winRef.successVideo){
    winRef.successVideo.style.display='block';
    //liveWindow.failVideo.onended = function(e){liveWindow.failVideo.style.display='none';liveWindow.videoBackground.style.display = 'block';};
    winRef.successVideo.play();
  }else{
    winRef.document.getElementById('roomCompleted').style.display = 'block';
  }
  // winRef.document.getElementById('successVideo').style.display = 'block';
  // winRef.document.getElementById('successVideo').play();
  timer_obj.stop();
  resetSoundtrack();
  playRoomSuccessSoundtrack();

  winRef.document.getElementById('completedRoomHeader').textContent = winRef.document.getElementById('countdown').innerHTML;

  resetBackgroundVideo();
  if (winRef.videoBackground) winRef.videoBackground.style.display = 'none';
  winRef.document.getElementById('photoClueContainer').style.display = 'none';
  $("#cd_start2").val("Start");

  winRef.document.getElementById('bodyMainContainerDiv').style.display = 'none';
  $('#roomLeaderboardModal').modal('show');
  gmStopRequestClueNotification();

  roomCompleted = true;
}

function soundtrackDonePlaying() {
  var soundTrackBtn = document.getElementById('gmplayandpause');
  soundTrackBtn.firstChild.className = 'fa fa-play-circle';
}

function playRoomSuccessSoundtrack(){
  if (winRef.successsoundTrack) winRef.successsoundTrack.play();
}

audioClue("");
function audioClue(audioID){
  $("#audioClueSlider").slider({
    value : (localStorage.getItem('acSlider'+room_id) || 75),
    step  : 1,
    range : 'min',
    min   : 0,
    max   : 100
  }).on("slidechange", function( event, ui ) {
    if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
    var value = $("#audioClueSlider").slider("value");
    if (audioID.length < 1)  return;
    localStorage.setItem('acSlider'+room_id, value);
    if(value < 5){
      winRef["clueAudio"+audioID].volume = 0;
    }else{
      winRef["clueAudio"+audioID].volume = (value / 100);
    }
  });
}

function backGroundVideo() {
  bgvidObject = winRef.document.getElementById("bgvidObject");
  backGroundVideoContainer = winRef.document.getElementById("backGroundVideoContainer");
  backSroundSource = winRef.document.getElementById("bgvidSrc");
  // if (winRef && winRef.videoBackground) winRef.videoBackground.pause();
}

function playRoomFailSoundtrack(){
  if (winRef.failedSoundTrack) winRef.failedSoundTrack.play();
}

//live audio transmission
function transmitAudioOnOff(this_obj){
  if(isLiveWindowOpen()){
    if(this_obj.hasClass('record_btn')){
      this_obj.removeClass('record_btn');
      this_obj.addClass('red_btn');
      this_obj.html('<span><i class="fa fa-microphone-slash" aria-hidden="true"></i></span> Transmitting...');
      winRef.startTransmittingAudio();
    }else{
      this_obj.removeClass('red_btn');
      this_obj.addClass('record_btn');
      this_obj.html('<i class="fa fa-microphone" aria-hidden="true"></i>');
      winRef.stopTransmittingAudio();
    }
  }
}

function hideShowOverlay() {
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  if(winRef.cachedOverlayImage) {
    if(!showOverlay){
      // winRef.document.getElementById('photoClueOutput').src = winRef.cachedOverlayImage;
      winRef.document.getElementById('photoClueContainer').style.display = 'block';
      $('#overlay').text('Hide Overlay');
      showOverlay = true;
      winRef.$('#bodyMainContainerDiv').hide();
    } else {
      hideOverlay();
    }
  }
}

function hideOverlay() {
  winRef.document.getElementById('photoClueContainer').style.display = 'none';
  $('#overlay').text('Show Overlay');
  showOverlay = false;
  winRef.$('#bodyMainContainerDiv').show();
}

var defaultTextColor = fontColor;
function changeSpeed(speed) {
  // RunRoomTimerController.speedTime(speed);
  timer_obj.speed = speed;
  if(isLiveWindowOpen()){
    if(speed == 1) {
      gmCounter.css('color', '#000000;');
      if(winLiveCounter) {
        winLiveCounter.css('color', defaultTextColor);
      }
    } else {
      gmCounter.css('color', 'red');
      if(winLiveCounter) {
        winLiveCounter.css('color', 'red');
      } else {
          winLiveCounter = winRef.$('#countdown');
          winLiveCounter.css('color', 'red');
      }
    }
  }
}

function completePuzzle(puzzleId) {
  var puzzleEl = $('.rm-puzzle-list input[value=' + puzzleId + ']');
  if (! puzzleEl.is(':checked')) {
    puzzleEl.click();
  }
}

function failRoom(){
    if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}

    if (roomCompleted) {
        console.log("Room is already complete!");
        return;
    }

    winRef.$('#bodyMainContainerDiv').hide();

    resetVideoClue();
    //if the fail video exists, play it

    if (winRef.failVideo){
      winRef.failVideo.style.display='block';
      //liveWindow.failVideo.onended = function(e){liveWindow.failVideo.style.display='none';liveWindow.videoBackground.style.display = 'block';};
      winRef.failVideo.play();
    }else{
      winRef.document.getElementById('timeExpiredNotification').style.display = 'block';
    }

    resetSoundtrack();

    playRoomFailSoundtrack();
    resetBackgroundVideo();
    if (winRef.videoBackground) winRef.videoBackground.style.display = 'none';
    winRef.document.getElementById('photoClueContainer').style.display = 'none';
    $('#roomLeaderboardModal').modal('show');

    if (!!winRef.document.getElementById('bgImageContainer')) winRef.document.getElementById('bgImageContainer').style.display = 'none';
    // winRef.document.getElementById('bgImageContainer').style.display = 'none';

    var cusRoomFailed = isEventExitsOrNot("roomFailed");
    customAutomationEvent("roomFailed", cusRoomFailed);

    gmStopRequestClueNotification();

    // Prevent completion from trigger in again
    roomCompleted = true;
}

function alterTime(timeToAdjust) {
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}

  if (roomCompleted) {
      console.log("Can't change timer when room is completed!");
      return;
  }

  if (roomCompleted) {
    console.log("Can't start timer when room is completed!");
    return;
  }

  timer_obj.adjustTime(timeToAdjust * 60 * 1000 * -1)
}

var cusRoomNtw = isEventExitsOrNot("networkPoll");
customAutomationEvent("networkPoll", cusRoomNtw);
customAutomationEvent('networkPoll');

function customAutomationEvent(cusType, filterList){
  if(filterList == undefined)  return;
  filterList.forEach(function(e){
    switch (cusType) {
      case "timeElapsed":
        var current_time = parseInt($("#id-start-time").val());
        var setElapsedTime = ((e.event.min * 60) + e.event.sec) * 100;
        var isElapsed = $.inArray(setElapsedTime, timeElapseList ) == -1;
        if (isElapsed && istimeElapse && current_time < setElapsedTime){
          timeElapseList.push(setElapsedTime);
          customActions(e.actions);
          istimeElapse = false;
        }

        if(isReuqestClueSent && current_time == setElapsedTime - 6000) gmStopRequestClueNotification();

        if(current_time < setElapsedTime) {
          istimeElapse = true;
        }
        break;
      case "timerStarted":
      case "timerStopped":
      case "roomCompleted":
      case "roomFailed":
      case "roomReset":
        customActions(e.actions);
        break;
      case "networkPoll":
        // netWorkPollingResult(e.event.url, e.event.poll_interval, e.actions);
        start(e);
        stop(e);
        reset(e);
        break;
      case "customButton":
        customActions(e.actions);
        break;
      case "customEvent":
        customActions(e.actions);
        break;
      default:console.log("unknown action type: "+ec.type);
    }
  });
}

function customActions(actions){
  if(!isLiveWindowOpen()) return;
  actions.forEach(function(ec){
    ectype = ec.type
    switch (ectype) {
      case "sendClueText":
        sendClueText(ec.clueText);
        break;
      case "playAlert":
        playAlertTone();
        break;
      case "playSound":
        playPauseAudioClue("sound"+ec.soundId);
        break;
      case "playVideo":
        playPauseVideoClue("video"+ec.videoId);
        break;
      case "displayImage":
        displayImageClue(ec.imageUrl);
        break;
      case "networkRequest":
        break;
      case "completePuzzle":
        completePuzzle(ec.puzzleId);
        break;
      case "philipsHue":
        recallScene(ec.group_id,ec.scene_id);
        break;
      case "philipsHueBlink":
        blinkGroup(ec.group,ec.interval,ec.duration);
        break;
      case "phHueOnOff":
        phGroupLightOnOffGroup(ec.group,ec.light_state);
      case "startTimer"  :
        timer_obj.start();
        break;
      case "stopTimer":
        timer_obj.stop();
        break;
      case "adjustTime":
        alterTime(ec.time_to_adjust);
        break;
      case "completeRoom":
        completeRoom();
        break;
      case "failRoom":
        stopTimer();
        failRoom();
        break;
      case "resetRoom":
        resetRoom();
        break;
      case "playIntroVideo":
        playPauseVideo();
        break;
      case "startSoundtrack":
        playSoundtrack();
        break;
      case "stopSoundtrack":
        pauseSoundtrack();
        break;
      case "customScript":
        eval(ec.script_text);
        break;
      case "requestCluefromGM":
        gmStartRequestClueNotification();
        break;
      default: console.log("unknown!action type: "+ec.type);
    }
  });
}

function gmStartRequestClueNotification(){
  $("#clearClueRequestBtn").show();
  $("#blinkCommunicationWindow h2").addClass("blink");
  $("#blinkCommunicationWindow h2").addClass("blink-room-communication-text");
  isReuqestClueSent = true;
}

$("#clearClueRequestBtn").click(function(){
  gmStopRequestClueNotification();
})

function gmStopRequestClueNotification(){
  $("#clearClueRequestBtn").hide();
  $("#blinkCommunicationWindow h2").removeClass("blink");
  $("#blinkCommunicationWindow h2").removeClass("blink-room-communication-text");
  isReuqestClueSent = false;
}

function isEventExitsOrNot(etype){
  var filterEventList = [];
  eventListJson.find(function(element) {
    if(element.event.type === etype){
      filterEventList.push(element);
    }
  });
  return filterEventList;
}

function isCustomEventExitsOrNot(etype, cuseventId){
  var cistFilterEventList = [];
  eventListJson.find(function(element) {
    if(element.event.type === etype && element.event.id==cuseventId){
      cistFilterEventList.push(element);
    }
  });
  return cistFilterEventList;
}

function customButtomAction(element){
  if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
  var cust_event_id = parseInt(element.attr("id"));
  var cus_actions = isCustomEventExitsOrNot("customButton",cust_event_id);
  cus_actions.forEach(function(cusAction){
    customActions(cusAction.actions);
  });
}

// window.onerror = function(error) {
//   // do something clever here
//   alert(error); // do NOT do this for real!
// };

function snapshotTime(){
  document.getElementById('gameMasterClueInput').value += gmCounter.text();
}

var is_delete = true;
function puzzleComplete(el) {
  var self = $(el);

  if (self.is(':checked')) {
    var startTime = parseInt($("#id-start-time").val());
    var defaultTimeLimit = parseInt(default_time_limit) * 60 * 100;
    if (startTime == '0'){
      solved_time = "00:00";
    }else{
      solved_time = formatTime(defaultTimeLimit - startTime);
    }
    helpers.ajaxCallback({
      url: URLS.users_room_summary,
      data: JSON.stringify({
        puzzle_id: parseInt(self.val()),
        solved_time: solved_time,
        play_count: parseInt(play_count) + 1,
        roomId: room_id,
        is_delete: is_delete
      }),
      success: function (res) {
        is_delete = false;
        var message_dialog = $("#message-dialog");
        message_dialog.find('p strong').html('Puzzle successfully solved!!');
        message_dialog.show();
        $(window).scrollTop($('#message-dialog').offset().top);
        message_dialog.fadeOut(10000);
      }
    });
  }
}

$("#saveleaderboards").click(function(){
  var teamName = $('#teamName').val();
  var numPlayers = $('#numPlayers').val();
  var cluesGiven = $('#cluesGiven').val();
  var consumed_time = $('#countdown').text();
  var tokens = consumed_time.split(':');
  var time_remaining = parseInt(tokens[0], 10) * 60 + parseInt(tokens[1], 10);

     $.ajax({
         url:URLS.save_room_details,
         type: "POST",
         data:{'team_name':teamName,'num_players':numPlayers,'num_clues':cluesGiven,'room':room_id,'time_remaining':time_remaining},
         success: function(response) {
             console.log('data saved');
         }

       });

  $("#puzzleprint").parent().show();
});

$(".nwp_box").hide();

cusRoomNtw.forEach(function(cusAction){
  switch (cusAction.event.url.split("/")[4]) {
      case "resume":
        start(cusAction);
        break;
      case "stop":
        stop(cusAction);
        break;
      case "reset":
        reset(cusAction);
        break;
      default: console.log("unknown!action type: ");

  }
});

function start(cusAction) {
  var test = "";
  // console.log("start")
  callCusRoomNtw('start', cusAction);
}

function stop(cusAction) {
  var test = "";
  // console.log("stop")
  callCusRoomNtw('stop', cusAction);
}

function reset(cusAction) {
  var test = "";
  // console.log("reset")
  callCusRoomNtw('reset', cusAction);
}


function callCusRoomNtw(callBackName, cusAction ){
  var test = "";
  if (!cusAction.event.url) return;

      test =
        $.ajax({
          type:'GET',
          url:cusAction.event.url,
          success:function(e){
            $(".nwp_box").show();
            $("#nwk-url").text(cusAction.event.url);
            $("#nwk-response").text(JSON.stringify(e));
            if(e.action == "triggered" && e.roomId == room_id){
              customActions(cusAction.actions);
            }
            setTimeout(eval(callBackName)(cusAction), cusAction.event.poll_interval);
          },
          error:function(e,n,o){
            setTimeout(eval(callBackName)(cusAction), cusAction.event.poll_interval);
          }
        });
}
// var count = 0;
// netWorkPollingResult(cusRoomNtw[count].event.url, cusRoomNtw[count].event.poll_interval, cusRoomNtw[count].actions)

// function netWorkPollingResult(nurl, p_interval, actions){
//   try{
//     var test =
//       $.ajax({
//         type:'GET',
//         url:nurl,
//         success:function(e){
//           $(".nwp_box").show();
//           $("#nwk-url").text(nurl);
//           $("#nwk-response").text(JSON.stringify(e));
//           if(e == "triggered"){
//             customActions(actions);
//           }
//           count++;
//           if (count < cusRoomNtw.length) {
//             netWorkPollingResult(cusRoomNtw[count].event.url, cusRoomNtw[count].event.poll_interval, cusRoomNtw[count].actions)
//           } else {
//             test = "";
//             count =0;
//             setInterval(function(){
//               netWorkPollingResult(cusRoomNtw[count].event.url, cusRoomNtw[count].event.poll_interval, cusRoomNtw[count].actions)
//             }, p_interval);

//           }
//         },
//         error:function(e,n,o){
//         }
//       });
//   }
//   catch (e) {
//   }
// }

// Philips Hue
var phUsername;
var phIpAddress;

function testConfig(){

  recallScene(
    $("#availableGroups option:selected").val(),
    $("#availableScenes option:selected").val()
  );
}

function recallScene(group, sce){
    $.ajax({
        method:"PUT",
        url:"http://"+phIpAddress+"/api/"+phUsername+"/groups/"+group+"/action",
        dataType:"json",
        data:JSON.stringify({scene:sce})
    }).done(function(e){
      console.log("done")
    });
}
function triggerPhilipsHue(event){
  recallScene($(event).parent()[0].attributes["data-group"].value, $(event).parent()[0].attributes["data-scene"].value);
}
function getBridgeData(){
  phUsername = phUsername;
  phIpAddress = phIpAddress;
  if(phSettings.length < 1) return;
  ph_settings = JSON.parse(phSettings.replace(/'/g, '"'));
  if (ph_settings) {
      // Needs drop down info populated from ajax calls, hence timer
      setTimeout(function () {
        $.each(ph_settings, function (index, value) {
            $('#philipsHueLights').append("<li class='scene' data-group='" + value.groupId + "' data-scene='" + value.sceneId + "'><a onClick='triggerPhilipsHue(this)'>" + $('#availableGroups option[value="' + value.groupId + '"]').text() + " - " + $('#availableScenes option[value="' + value.sceneId + '"]').text() + "</a></li>");
        });
      }, 500);
  }
}

getBridgeData();


// blinky lights code
function blinkSelectedGroupOnce() {
  blinkGroupOnce($("#availableGroups option:selected").val());
}

function blinkGroupOnce(group){
    $.ajax({
        method:"PUT",
        url:"http://"+phIpAddress+"/api/"+phUsername+"/groups/"+group+"/action",
        dataType:"json",
        data:JSON.stringify({"alert": "select"})
    }).done(function( html ) {
  });
}

function phGroupLightOnOffGroup(group, light_state){
    var new_light_state = (light_state == "1") ? true : false;
    $.ajax({
        method:"PUT",
        url:"http://"+phIpAddress+"/api/"+phUsername+"/groups/"+group+"/action",
        dataType:"json",
        data:JSON.stringify({"on": new_light_state})
    }).done(function( html ) {
  });
}

var blinkState = {};

function keepBlinking(group){
    var obj = blinkState[group];
    if(Date.now() > obj.blinkUntil){
        blinkGroupOnce(group);
        setTimeout(function() { keepBlinking(group); }, obj.blinkInterval);
    }
}

function blinkGroup(group, interval, duration) {
  var obj = {};
  obj.blinkUntil = Date.now() + parseInt(duration);
  obj.blinkInterval = parseInt(interval);

  if (blinkState[group] && Date.now() < blinkState[group].blinkUntil) {
    blinkState[group] = obj;
  } else {
    blinkState[group] = obj;
    keepBlinking(group);
  }
}
