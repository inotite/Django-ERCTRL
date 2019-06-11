var isValidUser = false;
var jsVars = roomJson;
var conn = io.connect('http://escaperoomctrl.com:3000/');
$(".wan-spinner-2").WanSpinner().css("border-color", "#2C3E50");

$(".page_left_panel").addClass("newpage_left_panel_hide");
$(".page_right_panel").addClass("newpage_right_panel_hide");

$(".menu_toogle a").click(function(){
  $(".page_left_panel").toggleClass('newpage_left_panel_hide');
  $(".page_left_panel").removeClass('page_left_panel_hide');
  $(".page_right_panel").removeClass('page_right_panel_hide');
  $(".page_right_panel").toggleClass('newpage_right_panel_hide');
});

serverConnected(false);

conn.on('connect', () => {
  conn.emit('messages', {type: "checkClient", roomId: room_id});
  serverConnected(true);
});

conn.on('disconnect', () => {
  serverConnected(false);
});

var gmCounter = $("#countdown");
var initialTimeMin =  jsVars.defaultTimeLimit;
var displayMs = jsVars.displayMs;

var timer = new Timer(initialTimeMin, displayMs, 1);

timer.addStartTimerCb(onTimerStart);
timer.addStopTimerCb(onTimerStop);
timer.addTimeUpdatedCb(onTimerUpdate);
timer.addTimeUpCb(onTimeUp);


var serverConnStatus = false;
var tabletConnStatus = false;

// Websocket

// messages
function sendTextClue(msgStr) {
    conn.emit('messages',{type:"text", msg:msgStr, roomId: room_id});
    $('#gameMasterClueInput').val("");
}

function sendStartTimer() {
    conn.emit('messages', {type: "startTimer", roomId: room_id});
}

function sendStopTimer() {
    conn.emit('messages', {type: "stopTimer", roomId: room_id});
}

function sendAlterTime(amount) {
    conn.emit('messages', {type: 'alterTime', amount: amount, roomId: room_id})
}

function sendResetRoom() {
    conn.emit('messages', {type: "resetRoom", roomId: room_id});
}

function sendCompleteRoom() {
    conn.emit('messages', {type: "completeRoom", roomId: room_id});
}

function sendPlayAlert() {
    conn.emit('messages', {type: "playAlert", roomId: room_id});
}

function sendClueCountMarketup(markupStr) {
    conn.emit('messages', {type: 'clueCountMarkup', markup: markupStr, roomId: room_id});
}

// socket setup
function handleServerMsg(data) {
    var incoming = data;
    switch (incoming.type) {
        case 'tabletOnline':
        case 'childlive':
            tabletConnected(incoming.status);
            break;
        case 'sendSuccess':
            console.log("Successfully sent: " + JSON.stringify(incoming.msg));
            break;
        case 'error':
            console.log("error sending: " + incoming.description);
            $('#errorSendingToTabletDlg').modal();
            break;
        default:
            console.log('Unknown msg type recieved: ' + incoming.type);
    }
}

conn.on('respond', function(data){
    $.ajax({
        type: "POST",
        url: URLS.token_validate,
        data: {'session_key': jsVars.userToken},
        success: function(response){
            var res_json = JSON.parse(response);
            if(res_json.status){
                isValidUser = true;
                if(parseInt(data.room) == parseInt(room_id)){
                    handleServerMsg(data);
                }
            }
        }
    });
});

function onTimerStart() {
    console.log('timer started');

    $('#cd_start2').val("Pause");
}

function onTimerStop() {
    console.log('timer stopped');

    $('#cd_start2').val("Start");
}

function onTimerUpdate() {
    var s = timer.displayStr();

    gmCounter.text(s);
}

function onTimeUp() {
    console.log('out of time');

    failRoom();
}

// Set initial time in GM view
onTimerUpdate();

// Send text to tablet
function updateClueText(clueText) {
    document.getElementById('gmLivePreviewText').textContent = clueText;
    sendTextClue(clueText);
}

// Timer start/stop btn
$('#cd_start2').on('click', function () {
    if (! canSendCommands()) return;

    if (timer.timeRemaining == 0) {
        alert('Room has ended, please reset!');
        return false;
    }
    if (timer.isRunning) {
        sendStopTimer();
    } else {

        sendStartTimer();
    }
    timer.toggle();
});

// reset room btn
function resetRoom() {
    if (! canSendCommands()) return;

    // Reset timer
    timer.stop();
    timer.reset();

    sendResetRoom();

    //reset clues notification elements
    resetClueCountDisplay();
    // I'll see you in hell

    //reset data feed
    $('#gameMasterClueInput').val("");
    // var awt = jsVars.initialDataFeedText;
    awt = "60";
    document.getElementById('gmLivePreviewText').textContent = awt;
}


function resetClueCountDisplay() {
  var $clueIcons = $('.gm-clue-element');
  $clueIcons.children().hide();
  $clueIcons.find('.gm-clue-off').show();
  updateLiveViewClueDisplay();
}

function updateLiveViewClueDisplay(){
    var markupStr = document.getElementById('gmClues').innerHTML;
    sendClueCountMarketup(markupStr);
}


// Press 'return' on clue area box
$("#gameMasterClueInput").bind("keypress", function(event) {
    if(event.which == 13 && !event.shiftKey) {
        event.preventDefault();
        sendMessageBtn();
    }
});

$('#gm-clear-clue-box').on('click', function () {
    clearLiveText();
});

$('#gmUpdateText').on('click', function () {
    sendMessageBtn();
});

// clear clue box btn
function clearLiveText() {
    if (! canSendCommands()) return;
    updateClueText('');
}


// send msg btn
function sendMessageBtn() {
    if (! canSendCommands()) return;

    var clueText = $('#gameMasterClueInput').val();
    updateClueText(clueText);
    $('#gameMasterClueInput').val("");
}

$('#completeRoom').on('click', function () {
    $('#roomSuccessLeaderboardModal').modal();
    completeRoom();
});

// complete room btn
function completeRoom() {
    if (! canSendCommands()) return;

    timer.stop();

    sendCompleteRoom();

    // $('#roomSuccessLeaderboardModal').modal();
}


// play alert btn
$('#gmAlertButton').on("click", function() {
    if (! canSendCommands()) return;

    sendPlayAlert();
});

$('#tb_reset_room').on("click", function() {
    if (! canSendCommands()) return;
    resetRoom();
});

// play alert btn
$('#gm-reset-room').on("click", function() {
    if (! canSendCommands()) return;
    $("#confirmResetRoom").modal({
      backdrop: 'static'
    });
});

$(document).on('click', "#tb_reset_room", function (event) {
  resetRoom();
});



// Clue list btn
$("#predefinedClues").click(function (event) {
    var clue = $(event.target)[0];
    document.getElementById('gameMasterClueInput').value = clue.text;
});


updateClueStatusEvtHandler('.gm-clue-off', '.gm-clue-on');
updateClueStatusEvtHandler('.gm-clue-on', '.gm-clue-used');
updateClueStatusEvtHandler('.gm-clue-used', '.gm-clue-off');


function updateClueStatusEvtHandler(currClass, nextClass) {
  $(currClass).click(function (event) {
    // if(!isLiveWindowOpen()){$('#pleaseOpenLiveView').modal();return;}
    var lock_type = currClass.split("-")[2];
    var lock_number = $(this).attr("data-lock-id");
    // if(isCheckBoolean(audio_alert_on_clue_count_change)) {playAlertTone();}
    var $this = $("#fa-"+lock_type+"-"+lock_number+"").closest(currClass);
    var $next = $this.closest('.gm-clue-element').find(nextClass);
    $this.hide();
    $next.show();
    var markupStr = document.getElementById('gmClues').innerHTML;
    sendClueCountMarketup(markupStr);
    // updateLiveViewClueDisplay(document.getElementById('gmClues').innerHTML);
  });
}

$("#btn-update-time").click(function (event) {
    var minutes = parseInt(document.getElementById('id-update-min').value);
    alterTime(minutes);
});
function alterTime(minutes) {
    if (! canSendCommands()) return;

    var amount = minutes * 60 * 1000 * -1;
    timer.adjustTime(amount);
    sendAlterTime(amount)
}

// Update UI based on server connection status
function serverConnected(connected) {
    var icon = $('#serverIndicator');
    if (connected) {
        icon.addClass('fa-circle ok-color');
        icon.removeClass('fa-exclamation-circle fail-color');
    } else {
        icon.removeClass('fa-circle ok-color');
        icon.addClass('fa-exclamation-circle fail-color');
    }
    serverConnStatus = connected;
}


// Update UI based on tablet connection tatus
function tabletConnected(connected) {
    var icon = $('#tabletIndicator');
    if (connected) {
        icon.addClass('fa-circle ok-color');
        icon.removeClass('fa-exclamation-circle fail-color');
    } else {
        icon.removeClass('fa-circle ok-color');
        icon.addClass('fa-exclamation-circle fail-color');
    }
    tabletConnStatus = connected;
}


// Can we actually send to the tablet???
function canSendCommands() {
    var connected = serverConnStatus && tabletConnStatus;

    function animate(s) {
        var factor = 200;
        $(s).fadeIn(factor).fadeOut(factor).fadeIn(factor).fadeOut(factor).fadeIn(factor);
    }

    if (! serverConnStatus) {
        animate("#serverIndicator");
    }

    if (! tabletConnStatus) {
        animate("#tabletIndicator");
    }
    return connected;
}


function saveLeaderboardData(teamName, numPlayers, cluesGiven){
    var secondsRemaining = timer.timeRemaining / 1000;
    var dataToSend = {};

    dataToSend.room_id = jsVars.roomId;
    dataToSend.time_remaining = secondsRemaining;

    if (teamName)
     dataToSend.team_name = teamName;

    function isInt(n){return n % 1 === 0;}

    if (numPlayers && isInt(numPlayers))
     dataToSend.num_players = numPlayers;

    if (cluesGiven && isInt(cluesGiven))
     dataToSend.num_clues = cluesGiven;

    //clear out team name field for next use
    $('#teamName').val('');
    $('#numPlayers').val('');
    $('#cluesGiven').val('');

    $.ajax({
      type: "POST",
      url: jsVars.leaderboardUrl,
      data: JSON.stringify(dataToSend),
      dataType: "JSON",
      contentType: "application/json"
    });
}


// Called when time is up
function failRoom(){
    $('#roomFailLeaderboardModal').modal();
}

window.onbeforeunload = function () {
    return "If you leave this page, the game session will terminate.";
};

$(window).bind('unload', function() {
});

// Close the side menu on open
setTimeout(function(){$('.sidebar-toggle').click();},50);
$('.sidebar-toggle').click();
