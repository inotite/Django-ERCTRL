$(document).ready(function() {

  generate_graph(local_data);

  // Add datetimepicker on from date and validation
  $("#id_from_date").datepicker({
    changeMonth: true,
    changeYear: true,
    format: "yyyy-mm-dd"
  }).change(fromDateChanged);

  // Add datetimepicker on to date and validation
  $("#id_to_date").datepicker({
    changeMonth: true,
    changeYear: true,
    format: "yyyy-mm-dd"
  }).change(toDateChanged);

  // Display analytics graph according to filter types(week, month, year) selection
  $("button.filter-btn").click(function(){
    var tracker_type = $(this).data("filter-type");
    $('#id_from_date').val("");
    $('#id_to_date').val("");
    $(this).parent().find("button").removeClass("active");
    $(this).addClass("active");
    $.ajax({
      type: "GET",
      url: URLS.ajax_user_tracker,
      data: {'tracker_type': tracker_type},
      success: function(response){
        generate_graph(response.tracker_list)
      }
    });
  });

  // Display analytics graph according to date range selection for js
  $(".generate-graph-btn").click(function(){
    var start_date = $('#id_from_date').val();
    var end_date = $('#id_to_date').val();
    $(".graph-filter-actions button.filter-btn").removeClass("active");
    $.ajax({
      type: "GET",
      url: URLS.ajax_user_tracker,
      data: {'start_date': start_date, 'end_date': end_date, 'tracker_type': 'date_range'},
      success: function(response){
        generate_graph(response.tracker_list)
      }
    });
  });

  function generate_graph(new_local_data){
    var opts = {
      axis: {
        "x": {
          "type": "category",
        },
        "y": {
          min: 1,
        }
      },
      zoom: { enabled: true },
    }

    var chart = bb.generate({
      "data": {
        "x": "timestamps",
        "columns": new_local_data,
        "types": {
          admin:"bar",
          user:"bar"
         }
      },
      axis: opts.axis,
      zoom: opts.zoom,
      "bindto": "#TimeseriesChart"
    });
  }

  function fromDateChanged(ev) {
    var to_date_length = $('#id_to_date').val().length;
    var next_date = new Date(ev.currentTarget.value);
    next_date.setDate(next_date.getDate() + 30);
    $('#id_to_date').datepicker('option', 'maxDate', next_date);
    if (to_date_length != 0){
      validate_to_and_from_date("frm_date");
    }
  }

  function toDateChanged(ev) {
    var frm_date_length = $('#id_from_date').val().length;
    var previous_date = new Date(ev.currentTarget.value);
    previous_date.setDate(previous_date.getDate() - 30);
    $('#id_from_date').datepicker('option', 'minDate', previous_date);
    if (frm_date_length != 0){
      validate_to_and_from_date("to_date");
    }
  }

  function validate_to_and_from_date(date_type){
    var from_date = moment($('#id_from_date').val());
    var to_date = moment($('#id_to_date').val());
    if (date_type=="frm_date" && from_date > to_date){
      if ($("#id_from_date").parent().find(".error-input").length < 1){
        $("#id_from_date").after("<span class='error-input'>From date must be less than or equal to date</span>");
      }
      $("#id_from_date").val("");
    }else{
      $("#id_from_date").parent().find(".error-input").remove();
    }
    if (date_type=="to_date" && to_date < from_date){
      if ($("#id_to_date").parent().find(".error-input").length < 1){
        $("#id_to_date").after("<span class='error-input'>To date must be grater than from date</span>");
      }
      $("#id_to_date").val("") ;
    }else{
      $("#id_to_date").parent().find(".error-input").remove();
    }
  }
});
