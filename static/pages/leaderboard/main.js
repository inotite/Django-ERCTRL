$(function() {

  if($('.room-leadership-slide').length > 0) {
    setTimeout(slideChange, scrollSpeed*1000);
    setTimeout(refreshPage, refreshInterval*1000);
  }

  if($('#newEntryCompleted').length) {
    $('#newEntryCompleted').datetimepicker({
        icons: {
      	  time: "fa fa-clock-o",
      	  date: "fa fa-calendar",
            up: "fa fa-arrow-up",
            down: "fa fa-arrow-down"
        },
        format: "MM/DD/YYYY HH:mm"
    });
  }

  $('body').on('changed.bs.select', '#entriesSelRoom', function(e) {
	 e.preventDefault();
	 var roomId = e.target.value;
	 console.log(roomId);
	 window.location.href = "/leaderboard/room/"+roomId+"/entries/";
  });

  $('body').on('click', '#entriesImportForm .btn-save', function(e) {
		e.preventDefault();
		var csvFile = $('#importFileName')[0].files[0];
    var fd = new FormData($('#entriesImportForm').get(0)); 
		// fd.append('room', $('#importSelRoom').val());
		fd.append('csvfile', csvFile);
		fd.append('csrfmiddlewaretoken', csrf_token);

		console.log(fd);

		if ( /\.(csv)$/i.test(csvFile.name) === false ) { 
			return 0;
		}
		
    $.ajax({
      type:"POST",
			cache:false,
			data: fd,
			contentType: false,
			processData: false,
			url: '/leaderboard/entries/save/',
			beforeSend:function(){
				console.log('beforesend');
			},
			success:function(result) {
					$('#importFileName').val('');
			},
			error:function(error, xhr, status) {
				console.log(status);
			}

    });

  });

  $('body').on('click', '.create-entry-wrapper .btn-save', function(e) {
	e.preventDefault();
    $('.create-entry-wrapper').find('.error').html('');

	var nplayers = $('#newEntryNumPlayers').val();
    if(/\D/.test(nplayers)) {
	  $('#newEntryNumPlayers').val('');
      $('#newEntryNumPlayers').closest('.field-wrapper').find('.error').html('Invalid input');
      return 0;
    }
	var nclues = $('#newEntryNumClues').val();
    if(/\D/.test(nclues)) {
	  $('#newEntryNumClues').val('');
      $('#newEntryNumClues').closest('.field-wrapper').find('.error').html('Invalid input');
      return 0;
    }

	var fd = new FormData();
	fd.append('name', $('#newEntryName').val());
	fd.append('time_left', $('#newEntryTimeLeft').val());
	fd.append('num_players', $('#newEntryNumPlayers').val());
	fd.append('num_clues', nclues);
	fd.append('room', $('#newEntryRoom').val());
	fd.append('completed', $('#newEntryCompleted').val());
	fd.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
      type:"POST",
	  cache:false,
	  data: fd,
	  contentType: false,
	  processData: false,
	  url: '/leaderboard/entry/create/',
	  beforeSend:function(){
      },
	  success:function(result) {
	    console.log(result);
		window.location.href = result.redirect;
      },
	  error:function(error) {

      },
	});

  });
  $('body').on('click', '.create-entry-wrapper .btn-edit', function(e) {
	e.preventDefault();
    console.log('Edit Entry');
    var key = $(this).closest('.create-entry-wrapper').data('value');
	var room = $('#newEntryRoom').val();
	console.log($('#newEntryName').val());
	console.log( $('#newEntryTimeLeft').val());
	 
	var fd = new FormData();
	fd.append('name', $('#newEntryName').val());
	fd.append('time_left', $('#newEntryTimeLeft').val());
	fd.append('num_players', $('#newEntryNumPlayers').val());
	fd.append('num_clues', $('#newEntryNumClues').val());
	fd.append('room', room);
	fd.append('completed', $('#newEntryCompleted').val());
	fd.append('csrfmiddlewaretoken', csrf_token);
    $.ajax({
      type:"POST",
	  cache:false,
	  data: fd,
	  contentType: false,
	  processData: false,
	  url: '/leaderboard/entry/edit/'+key+'/',
	  beforeSend:function(){
      },
	  success:function(result) {
		window.location.href = '/leaderboard/room/'+room+'/entries';
      },
	  error:function(error) {

      },
	});

  });



  $('body').on('click', '.lb-entry .link-delete', function(e) {
	var entry = $(this).closest('.lb-entry');
    var key = entry.data('value');
	var fd = new FormData();
	fd.append('key', key);
	fd.append('csrfmiddlewaretoken', csrf_token);

	$.confirm({
		'text': '<b>Do you want to delete ?</b>',
		confirm: function () {
	      $.ajax({
            type:"POST",            
			cache:false,
			data: fd,
			contentType: false,
			processData: false,
			url: '/leaderboard/entry/delete/',
			beforeSend:function(){
		    },
			success:function(result) {
              console.log(result);
			  entry.remove();
		    },
			error:function(error) {

		    }
		  });
		},
		cancel: function (button) {

	    },
		confirmButton: "Confirm",
		cancelButton: "Cancel"

	});

  });

  function slideChange() {
    var next = $('.room-leadership-slide.active').next();
	$('.room-leadership-slide.active').removeClass('active');
	if(next.length) {
      next.addClass('active');
    } else {
      $('.room-leadership-slide:first-child').addClass('active');
	}
    setTimeout(slideChange, scrollSpeed*1000);	
  }

  function refreshPage() {
     location.reload();
	 setTimeout(refreshPage, refreshInterval*1000);
  }


});

function checkextension(fname) {
}
