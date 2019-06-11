$(document).ready(function () {
    var recipients = $("#id_recipient");
    recipients.select2({
        width: '100%',
        allowClear: true,
        multiple: true,
        maximumSelectionSize: 1,
        placeholder: "Click here and start typing to search Recipients.",
        data: recipients_list  
    });
});

