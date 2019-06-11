window.onunload = refreshParent;
function refreshParent() {
    window.opener.set_winRef();
}

var host_url = window.location.origin;
var alertToneSound;
var soundtrackAudio;
var successsoundTrack;
var failedSoundTrack;
var videoBackground = document.querySelector('#bgvidObject');
// document.querySelector('#bgvidSrc');
var video = document.querySelector('#vidSrc');
// var successVideo = document.querySelector('#successVideo');
var successVideo = document.getElementById('successVideo');
var failVideo = document.getElementById('failVideo');
// var failVideo = document.querySelector('#failVideo');
// var successVideoUrl = window.opener.$("#videoBriefBtn").data('src');

var alert_tone_url = alertToneMediaUrl;
// window.opener.$("#gmAlertButton").data('src');
var soundtrack_audio_url = soundTrackAudioMediaUrl;
// window.opener.$("#gmplayandpause").data('src');
var success_sound_url = successAudioMediaUrl;
// window.opener.$("#gmSuccessAudio").data('src');
var failed_sound_url = failedAudioMediaUrl;
// window.opener.$("#gmFailedAudio").data('src');


var videoUrl = videoBriefMediaUrl;
var videoBriefSize;
var cachedVideoSize;
var isVideoBriefLoaded = false;

var videoBackgroundUrl = backgroundVideoMediaUrl;
var videoBackgroundSize;
var cachedVideoBackgroundSize;
var isVideoBackgroundLoaded = false;

var successVideoUrl = successVideoMediaUrl;
// document.getElementById('successVideoSrc').src;
var successVideoSize;
var cachedSuccessVideoSize = 0;
var isSuccessVideoLoaded = false;
var failVideoUrl = failVideoMediaUrl;
// document.getElementById('failVideoSrc').src;
var failVideoSize;
var cachedFailVideoSize = 0;
var isFailVideoLoaded = false;

var cachedOverlayImage = overlayImageMediaUrl;

var audios = [];

//localStorage.setItem('vbSlider'+roomId, 24);
//localStorage.setItem('bvSlider'+roomId, 24);
//localStorage.setItem('svSlider'+roomId, 24);
//localStorage.setItem('fvSlider'+roomId, 24);
// localStorage.setItem('atSlider'+roomId, 24);
//localStorage.setItem('stSlider'+roomId, 24);
//localStorage.setItem('acSlider'+roomId, 24);
localStorage.setItem('reSlider'+roomId, 24);
localStorage.setItem('vtSlider'+roomId, 24);
localStorage.setItem('vcSlider'+roomId, 24);

window.opener.$("#predefinedAudios button").each(function(){
    // $(this).data("sound-url")
    window["clueAudio"+$(this).attr("id")];
});

window.opener.$("#predefinedVideos button").each(function(){
    window["clueVideo"+$(this).attr("id")];
});

    navigator.getUserMedia = ( navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);

    function handleError(e) {
        // console.log(e);
      switch (e.code) {
      case FileError.QUOTA_EXCEEDED_ERR:
        log('QUOTA_EXCEEDED_ERR');
        break;
      case FileError.NOT_FOUND_ERR:
        log('NOT_FOUND_ERR');
        break;
      case FileError.SECURITY_ERR:
        log('SECURITY_ERR');
        break;
      case FileError.INVALID_MODIFICATION_ERR:
        log('INVALID_MODIFICATION_ERR');
        break;
      case FileError.INVALID_STATE_ERR:
        log('INVALID_STATE_ERR');
        break;
      default:
        log('Unknown error');
        break;
      }
    }

    if (navigator.getUserMedia) {
        navigator.getUserMedia({audio: true}, function(stream) {
            microphone = context.createMediaStreamSource(stream);
            microphone.volume = .1 || .75;
        }, audioerrorCallback);
    } else {
        console.log('navigator.getUserMedia not supported in this browser (probably Safari)');
    }

     //-------set up FileSystem stuff for caching-------------------------------------------------------
        window.requestFileSystem = window.requestFileSystem || window.webkitRequestFileSystem;
        window.resolveLocalFileSystemURL = window.resolveLocalFileSystemURL || window.webkitResolveLocalFileSystemURL;
        var requestedBytes = 1024 * 1024 * 4096;

        if (navigator.webkitPersistentStorage) {
            navigator.webkitPersistentStorage.requestQuota(
                requestedBytes,
                function(grantedBytes) {
                    console.log(grantedBytes, 'bytes granted.');
                },
                function(e) { console.log('Error', e); }
            );
        } else {
            console.log('Persistent storage init not being called because you are not using Chrome!!')
        }

        window.requestFileSystem(window.PERSISTENT, requestedBytes, handleInitSuccess, function(e){console.log(e);});


    $(document).on("click", function() { var el = document.documentElement , rfs = el.requestFullScreen || el.webkitRequestFullScreen || el.mozRequestFullScreen ; rfs.call(el); });
//------fun stuff for live audio transmission-------------------------------------------------------------------
    window.AudioContext = window.AudioContext || window.webkitAudioContext;

    var context = new AudioContext();
    var microphone;
    var filter;

    // TODO: use this!
    var biquadFilterValue = mic_biquad_filter ;

    function audioerrorCallback(){console.log("error callback error");}

    function startTransmittingAudio(){
        //user for filtering some of the tingyness out of audio
        filter = context.createBiquadFilter();
        if (filter && microphone) microphone.connect(filter);
        //if (filter) filter.connect(context.destination);
        switch(biquadFilterValue) {
        case "Off":
                microphone.connect(context.destination);
                break;
        case "lowpass":
                filter.type = "lowpass"
                break;
        case "highpass":
                filter.type = "highpass"
                break;
        case "bandpass":
                filter.type = "bandpass"
                break;
        case "lowshelf":
                filter.type = "lowshelf"
                break;
        case "highshelf":
                filter.type = "highshelf"
                break;
        case "peaking":
                filter.type = "peaking"
                break;
        case "notch":
                filter.type = "notch"
                break;
        case "allpass":
                filter.type = "allpass"
                break;
        case"On":
        default:
            filter.connect(context.destination);
        }

    }
    function stopTransmittingAudio(){
        if (microphone) microphone.disconnect(0);
        if (filter) filter.disconnect(0);
    }

    function addLiveViewListenener() {
        soundtrackAudio.addEventListener('ended', function(e) {
            var gmRoomView = window.opener;
            if (gmRoomView) gmRoomView.soundtrackDonePlaying();
        });
    }
     //---end live audio transmission stuff---
    var promises = [];
    function handleInitSuccess(fileSystem) {
        window.fileSystem = fileSystem;

        if(videoUrl) {
			var vbVal = localStorage.getItem('vbSlider'+roomId);
			if (vbVal == null || vbVal == '') {
              vbVal = 24;
			  localStorage.setItem('vbSlider'+roomId, vbVal);
	        }
			var volume = (vbVal == 0) ? 0 : ((vbVal/100) || .75);
            video.volume = volume;
        }
        promises.push(new Promise(function(resolve, reject) {
            video_duration = $("#videoBriefObject")
            new Cacher(videoUrl, 'videoBriefProgress').cache(function(url) {
                if(url) {
                    isVideoBriefLoaded = true;
                    video.src = url;
                    document.getElementById('videoBriefObject').load();
                    resolve('Successfully Loaded Video');
                } else {
                    resolve('We Failed, but we did not');
                }
            });
        }));
        if(videoBackgroundUrl) {
			var bvVal = localStorage.getItem('bvSlider'+roomId); 
			if (bvVal == null || bvVal == '') {
              bvVal = 24;
			  localStorage.setItem('bvSlider'+roomId, bvVal);
		    }
			var volume = (bvVal == 0) ? 0 : ((bvVal/100) || .75);
            videoBackground.volume = volume;
        }
        promises.push(new Promise(function(resolve, reject) {
            new Cacher(videoBackgroundUrl, 'backgroundVideoProgress').cache(function(url) {
                if(url) {
                    isVideoBackgroundLoaded = true;
                    videoBackground.src = url;
                    document.getElementById('bgvidObject').load();
                    resolve('Loaded background video');
                } else {
                    resolve('We Failed, but we did not');
                }
            });
        }));
        if(successVideoUrl) {
			var svVal = localStorage.getItem('svSlider'+roomId);
			if(svVal == null || svVal == '') {
			  svVal = 24;
			  localStorage.setItem('svSlider'+roomId, svVal);
		    }
			var volume = (svVal == 0) ? 0 : ((svVal/100) || .75);
            successVideo.volume = volume;
        }
        promises.push(new Promise(function(resolve, reject) {
            new Cacher(successVideoUrl, 'successVideoProgress').cache(function(url) {
                if(url) {
                    isSuccessVideoLoaded = true;

                    successVideo.src = url;
                    document.getElementById('successVideo').load();
                    resolve('Loaded success video');
                } else {
                    resolve('We Failed, but we did not');
                }
            });
        }));
        if(failVideoUrl) {
			var fvVal = localStorage.getItem('fvSlider'+roomId);
			if(fvVal == null || fvVal == '') {
              fvVal = 24;
			  localStorage.setItem('fvSlider'+roomId, fvVal);
		    }
			var volume = (fvVal == 0) ? 0 : ((fvVal/100) || .75);
            failVideo.volume = volume;
        }
        promises.push(new Promise(function(resolve, reject) {
            new Cacher(failVideoUrl, 'failVideoProgress').cache(function(url) {
                if(url) {
                    isFailVideoLoaded = true;

                    failVideo.src = url;
                    document.getElementById('failVideo').load();
                    resolve('loaded fail video successfully')
                } else {
                    resolve('We Failed, but we did not');
                }
            });
        }));

        promises.push(new Promise(function(resolve, reject) {
            new Cacher(success_sound_url, 'successSoundtrackProgress').cache(function(url) {
                if(url) {
                    successsoundTrack = new Audio(url);
                    successsoundTrack.volume = localStorage.getItem('svSlider'+roomId)/100 || .75;
                    successsoundTrack.load();
                    resolve('Loaded success soundtrack')
                } else {
                    resolve('We Failed, but we did not');
                }
            });
        }));

        promises.push(new Promise(function(resolve, reject) {
            new Cacher(failed_sound_url, 'failSoundtrackProgress').cache(function(url) {
                if(url) {
                    failedSoundTrack = new Audio(url);
                    failedSoundTrack.load();
                    resolve('Loaded fail soundtrack')
                } else {
                    resolve('We Failed, but we did not');
                }
            });
        }));


        promises.push(new Promise(function(resolve, reject ) {
			var atVal = localStorage.getItem('atSlider'+roomId);
			if (atVal == null || atVal == '') {
			  atVal = 24;
              localStorage.setItem('atSlider'+roomId, atVal);
			}
            new Cacher(alert_tone_url, 'alertToneProgress').cache(function(url) {
                if(url) {
                    alertToneSound = new Audio(url);
				    var volume = (atVal == 0) ? 0 : ((atVal/100) || .75);	
                    alertToneSound.volume = volume;
                    resolve('Success')
                } else {
                    resolve('We Failed, but we did not');
                }
            });
        }));

        promises.push(new Promise(function(resolve, reject) {
			var stVal = localStorage.getItem('stSlider'+roomId);
			if (stVal == null || stVal == '') {
				console.log('setting default');
				stVal = 24;
				localStorage.setItem('stSlider'+roomId, stVal);
	        }
            new Cacher(soundtrack_audio_url, 'soundtrackProgress').cache(function(url) {
                if(url) {
                    soundtrackAudio = new Audio(url);
					if (stVal == 0) {
						soundtrackAudio.volume = 0;
					} else {
                        soundtrackAudio.volume = localStorage.getItem('stSlider'+roomId)/100 || .75;
				    }
                    addLiveViewListenener();
                    resolve('Success')
                } else {
                    resolve('We Failed, but we did not');
                }
            });
        }));

        window.opener.$("#predefinedVideos button").each(function(){
            var videoID = $(this).attr("id") ;
            var clue_video_url = host_url + $(this).data("video-url");
            promises.push(new Promise(function(resolve, reject) {
                new Cacher(clue_video_url, 'video'+videoID+'Progress').cache(function(url) {
                    if(url) {
                        window['clueVideo'+videoID] = url;
                        resolve('Loaded video '+videoID.split('video')[1]+'')
                    } else {
                        resolve('We Failed, but we did not');
                    }
                });
            }));
        });

        window.opener.$("#predefinedAudios button").each(function(){
            var soundID = $(this).attr("id") ;
            var clue_audio_url = host_url + $(this).data("sound-url") ;
            promises.push(new Promise(function(resolve, reject) {
				var acVal = localStorage.getItem('acSlider'+roomId);
				if (acVal == null || acVal == '') {
                  acVal = 24;
				  localStorage.setItem('acSlider'+roomId, acVal);
				}
                new Cacher(clue_audio_url, 'sound'+soundID+'Progress').cache(function(url) {
                    if(url) {
					var volume = (acVal == 0) ? 0 : ((acVal/100) || .75);
                    window['clueAudio'+soundID] = new Audio(url);
                    window['clueAudio'+soundID].volume = volume;
                    window['clueAudio'+soundID] = eval('clueAudio'+soundID);
                    resolve('Success');
                } else {
                    console.log('failed to load');
                    resolve('We Failed, but we did not');
                }
                });
            }));
        });

        Promise.all(promises).then(function(values) {
            if (window.opener && window.opener.document) {
                window.opener.$('#loadingAssets').modal('hide');
            }
        }).catch(function(errors) {
            // console.log(errors);
        });
    }

if (failVideo != null){
    failVideo.onended = function(e){
        failVideo.currentTime = 0;
        failVideo.style.display = 'none';
        // Show normal fail screen once video completes
        document.getElementById('timeExpiredNotification').style.display = 'block';
    };
}

if (successVideo != null){
    successVideo.onended = function(e){
        successVideo.currentTime = 0;
        successVideo.style.display = 'none';
        // Show normal success screen once video completes
        document.getElementById('roomCompleted').style.display = 'block';
    };
}

var style = document.createElement('style');
style.type = 'text/css';
style.innerHTML = '';
if (endGameSuccessBackgroundMediaUrl.length > 0) style.innerHTML += '.room-success-screen { background: url('+endGameSuccessBackgroundMediaUrl+') no-repeat center center fixed; background-size: 100% 100%;}';
if (failureBackgroundImageMediaUrl.length > 0) style.innerHTML += '.room-failure-screen { background: url('+failureBackgroundImageMediaUrl+') no-repeat center center fixed; background-size: 100% 100%;}';
if (style.innerHTML.length > 0) document.getElementsByTagName('head')[0].appendChild(style);
