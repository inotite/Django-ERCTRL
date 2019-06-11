function log(text) {console.log(text);}
var conn = io.connect('http://escaperoomctrl.com:3000/');
var jsVars = roomJson;
var liveViewAudioAlert = new Audio(jsVars.audioAlertUrl);
var isValidUser = false;

conn.on('respond', function(data){
    if(data.type == "checkClient"){
        conn.emit('messages', {type: "childlive", status: true, roomId: jsVars.room_id});
    }else{
        $.ajax({
            type: "POST",
            url: URLS.token_validate,
            data: {'session_key': jsVars.userToken},
            success: function(response){
                var res_json = JSON.parse(response);
                if(res_json.status && (parseInt(data.room) == parseInt(jsVars.room_id))){
                    isValidUser = true;
                    handleServerMsg(data);
                }
            }
        });
    }
});

$(window).unload(function() {
    conn.emit('messages', {type: "tabletOnline", "status": false, roomId: jsVars.room_id});
});

function connectTab(){
    conn.emit('messages', {type: "tabletOnline", status: true , roomId: jsVars.room_id});
}

connectTab()

function handleServerMsg(data) {
    var incoming = data;
    switch (incoming.type) {
        case "text":
            console.log("Text message received with a content of - " + incoming.msg);
            $('#communicationText').text(incoming.msg);

            if (jsVars.audioAlertOnClueSend && incoming.msg != '') liveViewAudioAlert.play();

            break;
        case 'startTimer':
            timer.start();
            break;
        case 'stopTimer':
            timer.stop();
            break;
        case 'resetRoom':
            timer.stop();
            timer.reset();

            // Reset clue box
            $('#communicationText').text(jsVars.initialDataFeedText);

            // Close success block
            document.getElementById('roomCompleted').style.display = 'none';

            // Close fail block
            document.getElementById('timeExpiredNotification').style.display = 'none';

            break;
        case 'completeRoom':
            timer.stop();

            // Set the time elapsed
            document.getElementById('completedRoomHeader').textContent = document.getElementById('countdown').innerHTML;

            // Display success msg
            document.getElementById('roomCompleted').style.display = 'block';
            document.getElementById('bodyMainContainerDiv').style.display = 'none';
            break;
        case 'playAlert':
            liveViewAudioAlert.play();
            break;
        case 'alterTime':
            timer.adjustTime(incoming.amount);
            break;
        case 'clueCountMarkup':
            document.getElementById('liveClueDisplay').innerHTML = incoming.markup;
            break;
        default:
            console.log('Unknown msg type recieved: ' + incoming.type);
    }
}

var liveCounter = $('#countdown');

var initialTimeMin =  jsVars.defaultTimeLimit;
var displayMs = jsVars.displayMs;

var timer = new Timer(initialTimeMin, displayMs, 1);

timer.addStartTimerCb(onTimerStart);
timer.addStopTimerCb(onTimerStop);
timer.addTimeUpdatedCb(onTimerUpdate);
timer.addTimeUpCb(onTimeUp);

function onTimerStart() {
    console.log('timer started');
}

function onTimerStop() {
    console.log('timer stopped');
}

function onTimerUpdate() {
    var s = timer.displayStr();

    liveCounter.text(s);
}

function onTimeUp() {
    console.log('out of time');

    document.getElementById('timeExpiredNotification').style.display = 'block';
}

// Set initial time HTML
onTimerUpdate();



// Set the initial time on load
if (window.opener && window.opener.timer) window.document.getElementById('liveTimeRemaining').textContent = window.opener.timer.displayStr();
