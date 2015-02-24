// http://blog.teamtreehouse.com/create-ajax-contact-form

$(function() {

    // Get the form.
    var form = $('#contact-form');

    // Get the messages div.
    var formMessages = $('#form-messages');

    // Error message if something goes wrong.
    var errorMessage = '<strong>Oops!</strong> An error occured and your message could not be sent.';

    // Set up an event listener for the contact form.
    $(form).submit(function(e) {
        // Stop the browser from submitting the form.
        e.preventDefault();

        // Detect bots.
        if($('#honeypot').val() != '') {
           $(formMessages).html(errorMessage);
           return;
        }

        // Serialize the form data.
        var formData = $(form).serialize();

        // Submit the form using AJAX.
        $.ajax({
            type: 'POST',
            url: $(form).attr('action'),
            data: formData
        })
        .done(function(response) {
            // Make sure that the formMessages div has the 'success' class.
            $(formMessages).removeClass('alert alert-danger');
            $(formMessages).addClass('alert alert-success');

            // Set the message text.
            $(formMessages).html(response);

            // Clear the form.
            $('#honeypot').val('');
            $('#name').val('');
            $('#email').val('');
            $('#message').val('');
            $('#sendcopy').attr('checked', false);
        })
        .fail(function(data) {
            // Make sure that the formMessages div has the 'error' class.
            $(formMessages).removeClass('alert alert-success');
            $(formMessages).addClass('alert alert-danger');

            // Set the message text.
            if (data.responseText !== '') {
                $(formMessages).html(data.responseText);
            } else {
                $(formMessages).html(errorMessage);
            }
        });
    });
});
