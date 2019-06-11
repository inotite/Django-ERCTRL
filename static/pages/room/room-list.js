// Add clear cache for js
// $(document).on("click", ".clear-cache-btn", function (e) {
//   $.ajax({
//     url: URLS.clear_cache,
//     type: 'GET',
//     enctype: "multipart/form-data",
//     processData: false,
//     contentType: false,
//     cache: false,
//     success: function (response) {
//       var message_dialog = $("#message-dialog");
//       message_dialog.find('p strong').html(response['messages']);
//       message_dialog.show();
//       $(window).scrollTop($('#message-dialog').offset().top);
//       message_dialog.fadeOut(10000);
//     },
//     error: function (res) {
//       alert("Error: " + res.responseText);
//     }
//   });
//   return false;
// });

$(document).on("click", ".clear-cache-btn", function (e) {
  $('#confirmClearCache').modal();
});

$(".oflinemode_btn").click(function(){
  requestCache();
});

// Delete room for js
  $("a.delete-room").click(function(){
    var link = $(this);
    // debugger
    // e.stopPropagation();
    // e.preventDefault();
    $.confirm({
      'text': '<b>Are you sure?</b>',
      confirm: function () {
          $.ajax({
              type: "POST",
              url: URLS.room_delete.replace('11111111', link.data("room-id")),
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



  window.requestFileSystem = window.requestFileSystem || window.webkitRequestFileSystem;
    window.resolveLocalFileSystemURL = window.resolveLocalFileSystemURL || window.webkitResolveLocalFileSystemURL;
    function errorHandler(e) {
     var msg = '';

     switch (e.code) {
       case FileError.QUOTA_EXCEEDED_ERR:
         msg = 'QUOTA_EXCEEDED_ERR';
         break;
       case FileError.NOT_FOUND_ERR:
         msg = 'NOT_FOUND_ERR';
         break;
       case FileError.SECURITY_ERR:
         msg = 'SECURITY_ERR';
         break;
       case FileError.INVALID_MODIFICATION_ERR:
         msg = 'INVALID_MODIFICATION_ERR';
         break;
       case FileError.INVALID_STATE_ERR:
         msg = 'INVALID_STATE_ERR';
         break;
       default:
         msg = 'Unknown Error';
         break;
     };

     console.log('Error: ' + msg);
    }
    function toArray(list) {
     return Array.prototype.slice.call(list || [], 0);
    }

    function listResults(entries) {
     entries.forEach(function(entry, i) {entry.remove(function(){},errorHandler);});
    }

    function onInitFs(fs) {
     var dirReader = fs.root.createReader();
     var entries = [];

     // Call the reader.readEntries() until no more results are returned.
     var readEntries = function() {
        dirReader.readEntries (function(results) {
         if (!results.length) {
           listResults(entries.sort());
         } else {
           entries = entries.concat(toArray(results));
           readEntries();
         }
       }, errorHandler);
     };
     readEntries(); // Start reading dirs.
    }

    function deleteAllEntries(){
      window.requestFileSystem(window.PERSISTENT, 1024*1024, onInitFs, errorHandler);
      $(".close").click();
    }
    function requestCache(){
        window.requestFileSystem = window.requestFileSystem || window.webkitRequestFileSystem;
        window.resolveLocalFileSystemURL = window.resolveLocalFileSystemURL || window.webkitResolveLocalFileSystemURL;
        var requestedBytes = 1024 * 1024 * 4096;

        if (navigator.webkitPersistentStorage) {
            navigator.webkitPersistentStorage.requestQuota(
                requestedBytes,
                function(grantedBytes) {
                    if(grantedBytes<1)
                        $('#cacheFailure').modal();
                    else
                        $('#cacheSuccess').modal();
                },
                function(e) { console.log('Error', e);$('#cacheFailure').modal(); }
            );
        } else {
            $('#cacheFailure').modal();
        }
        window.requestFileSystem(window.PERSISTENT, requestedBytes, function(){}, function(e){console.log(e);});
    }