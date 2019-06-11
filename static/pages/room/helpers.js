(function(window){

    var csrftoken = getCookie('csrftoken'),
        $progressButton;
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            $progressButton && $progressButton.progressInitialize().blur();
        },
        complete: function () {
            $progressButton && $progressButton.progressFinish();
        },
        xhr: function () {
            var xhr = new window.XMLHttpRequest(),
                percentComplete;
            if ($progressButton) {
                // Upload progress
                xhr.upload.addEventListener("progress", function (evt) {
                    if (evt.lengthComputable) {
                        percentComplete = Math.ceil(evt.loaded / evt.total * 100);
                        $progressButton.progressIncrement(percentComplete);
                    }
                }, false);
            }
           return xhr;
        }
    });

    $('body').on('change', 'input[type="file"]', function () {
        return helpers.validateImage(this);
    }).on('click', '.progress-button', function () {
        $progressButton = $(this);
    });

    window.helpers = {
        submitForm: function (formId, cbSuccess, cbError, reset, cbMethod, formDataFn) {
            $('body').on('submit', formId, function (e) {
                e.preventDefault();
                var $form = $(this),
                    successClass = 'success',
                    errorClass = 'error',
                    url = $.trim($form.attr('action')),
                    method = cbMethod || $form.attr('method'),
                    formData = new FormData($form[0]);

                $form.find('[type="submit"]').prop("disabled", true);

                $.ajax({
                    url: url,
                    type: method,
                    dataType: 'json',
                    data: formDataFn ? formDataFn() : formData,
                    contentType: false,
                    processData: false,
                    statusCode: {
                        '500': function () {
                            helpers.displayMessage('Something went wrong', errorClass);
                        },
                        '403': function (res) {
                            helpers.displayMessage(res.responseJSON.detail, errorClass);
                        }
                    },
                    success: function (res) {
                        $form.find('[type="submit"]').prop("disabled", false);
                        if (typeof cbSuccess === 'function') {
                            cbSuccess(res, $form);
                        } else {
                            helpers.displayMessage('Successfully saved', successClass);
                        }
                        $form.find('.has-error').removeClass('has-error');
                        $form.find('.help-block').remove();
                        if (!reset)
                            $form.trigger('reset');
                    },
                    error: function (res) {
                        var errors = '';

                        switch (true) {
                            case ( !!res.responseJSON && !!res.responseJSON.errors ):
                                errors = res.responseJSON.errors;
                                break;

                            case ( !!res.responseJSON ):
                                errors = res.responseJSON;
                                break;
                        }

                        if (typeof cbError === 'function') {
                            cbError(res, $form);
                        }

                        $form.find('[type="submit"]').prop("disabled", false);
                        $form.removeClass('loading');
                        if ($.isArray(errors)){
                            $form.find('.has-error').removeClass('has-error');
                            $form.find('ul.help-block').remove();
                            errors.forEach(function (item, i) {
                                helpers.setErrors(item, $form, null, true, 'form-' + i + '-');
                            });
                        } else {
                            helpers.setErrors(errors, $form);
                        }
                    }
                });
            });
        },
        setErrors: function ( errors, form, errorClass, hideErrors, prefix ) {
            var $form = $( form ),
                errorsKeys = !!errors ? Object.keys( errors ) : [];

            errorClass = !!errorClass ? errorClass : 'help-block';
            prefix = prefix || '';

            if (!hideErrors) {
                $form.find('ul.' + errorClass).remove();
            }
            for ( var i = 0; i < errorsKeys.length; i++ ) {
                var key = errorsKeys[i],
                    err = errors[key],

                    length = err.length,
                    $formfield = $form.find( '[name="' + prefix + key + '"]' ),
                    formfieldParent = $formfield.parents('.form-group'),
                    template = '',
                    errorsList;

                if ( !$formfield.length ) {
                    helpers.displayMessage(err, 'error');
                    continue;
                }

                for ( var j = 0; j < length; j++ ) {
                    template += helpers.messageTemplate( err[j] );
                }

                errorsList = '<ul class="' + errorClass + '">' + template + '</ul>';

                $formfield.after( errorsList );

                formfieldParent.addClass('has-error')
            }
        },
        displayMessage: function (text, alertClass) {
            notie.alert(alertClass, text, 3)
        },
        messageTemplate: function(message) {
            return '<li>' + message + '</li>';
        },
        ajaxCallback: function (data) {
            $.ajax({
                url: data.url,
                type: data.type || 'POST',
                data: data.data,
                dataType: (data.hasOwnProperty('dataType')) ? data.dataType : 'json',
                processData: false,
                contentType: (data.hasOwnProperty('contentType')) ? data.contentType : 'application/json',
                success: function (resp) {
                    if (data.success)
                        data.success(resp);
                },
                error: function (resp) {
                    if (data.error)
                        data.error(resp);
                }
            });
        },
        formatSizeUnits: function (bytes){
            if      (bytes>=1024 * 1024 * 1024) {bytes=(bytes/(1024 * 1024 * 1024)).toFixed(0)+'Gb';}
            else if (bytes>=1024 * 1024)        {bytes=(bytes/(1024 * 1024)).toFixed(0)+'Mb';}
            else if (bytes>=1024)               {bytes=(bytes/1024).toFixed(0)+'Kb';}
            else if (bytes>1)                   {bytes=bytes+'bytes';}
            else if (bytes==1)                  {bytes=bytes+'byte';}
            else                                {bytes=0;}
            return bytes;
        },
        validateImage: function(el){
            var fileInput,
                allowedFileSize = CONFIG.ALLOWED_IMAGE_FILE_SIZE,
                errors = [],
                error = {},
                $this = $(el),
                $el = $this.parents('.form-group'),
                files = el.files || [];

            $el.removeClass('has-error');
            $el.find('.help-block').remove();
            for (var i=0; i<files.length; i+=1){
                fileInput = files[i];
                if (fileInput.name.match(/\.(jpg|jpeg|png|gif)$/) &&
                  (fileInput.size > allowedFileSize || fileInput.fileSize > allowedFileSize)) {
                    error[$this.attr('name')] = ['Allowed file size exceeded. Image file size should less or equal ' +
                                                 helpers.formatSizeUnits(allowedFileSize)];
                    helpers.setErrors(error, $el);
                    errors.push(fileInput.name)
                }
            }
            if (errors.length && errors.length == files.length){
                el.value = null;
                return false;
            }
            return true;
        }
    }
})(this);
