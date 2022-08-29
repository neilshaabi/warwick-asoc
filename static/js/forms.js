$(document).ready(function(){

    // Toggles loading button
    function showLoadingBtn(isLoading) {
        if (isLoading == true) {
            $(':input[type="submit"]').prop('disabled', true);
            $('.btn-text').hide();
            $('.spinner-border').show();
        } else {
            $(':input[type="submit"]').prop('disabled', false);
            $('.btn-text').show();
            $('.spinner-border').hide();
        }
    }


    // Registration handler using AJAX
    $('#register-form').on('submit', function(event) {

        showLoadingBtn(true);

        $.post(
            '/register', 
            {'first_name' : $('#first_name').val(), 'last_name' : $('#last_name').val(), 
             'email' : $('#email').val(), 'password' : $('#password').val()}, 
            function(data) {
            
                // Display error message if unsuccessful
                if (data.error) {
                    showLoadingBtn(false);
                    $('#error-alert').html(data.error).show();
                } 
                
                // Reload page if successful
                else {
                    window.location = data;
                }
            }
        );
        event.preventDefault();
    });
    

    // Login handler using AJAX
    $('#login-form').on('submit', function(event) {

        showLoadingBtn(true);

        $.post(
            '/login', 
            {'email' : $('#email').val(), 'password' : $('#password').val()}, 
            function(data) {
            
                // Display error message if unsuccessful
                if (data.error) {
                    showLoadingBtn(false);
                    $('#error-alert').html(data.error).show();
                } 
                
                // Redirect to home page if successful
                else {
                    window.location = data;
                }
            }
        );
        event.preventDefault();
    });


    // Resend email verification handler using AJAX
    $('#verify-email-form').on('submit', function(event) {

        showLoadingBtn(true);

        $.post(
            '/verify-email', 
            {'email' : $('#email').val()}, 
            function(data) {
                showLoadingBtn(false);
            }
        );
        event.preventDefault();
    });


    // Password reset request handler using AJAX
    $('#reset-request-form').on('submit', function(event) {

        showLoadingBtn(true);
        
        $.post(
            '/reset-password', 
            {'form-type' : 'request', 'email' : $('#email').val()}, 
            function(data) {
            
                // Display error message if unsuccessful
                if (data.error) {
                    showLoadingBtn(false);
                    $('#error-alert').html(data.error).show();
                } 
                
                // Redirect to home page if successful
                else {
                    window.location = data;
                }
            }
        );
        event.preventDefault();
    });


    // Password reset handler using AJAX
    $('#reset-password-form').on('submit', function(event) {

        $.post(
            '/reset-password', 
            {'form-type' : 'reset', 'email' : $('#email').val(),
             'password' : $('#password').val(), 'password_confirmation' : $('#password-confirmation').val()}, 
            function(data) {
            
                // Display error message if unsuccessful
                if (data.error) {
                    $('#error-alert').html(data.error).show();
                } 
                
                // Redirect to home page if successful
                else {
                    window.location = data;
                }
            }
        );
        event.preventDefault();
    });


    // Account settings edits handler using AJAX
    $('#settings-form').on('submit', function(event) {

        // Get student ID if it exists
        var student_id = null;
        if ($('#membership-type').html() == 'Student') {
            student_id = $('#student_id').val();
        }

        $.post(
            '/settings', 
            {'first_name' : $('#first_name').val(), 'last_name' : $('#last_name').val(), 
             'email' : $('#email').val(), 'student_id' : student_id}, 
            function(data) {
            
                // Display error message if unsuccessful
                if (data.error) {
                    $('#error-alert').html(data.error).show();
                } 
                
                // Reload page if successful
                else {
                    window.location = data;
                }
            }
        );
        event.preventDefault();
    });

    
    // Membership selection handler using AJAX
    $('#membership-form').on('submit', function(event) {

        event.preventDefault();
        showLoadingBtn(true);
        
        // Displays error message if user is not logged in or already a member
        if ($('#membership-btn').attr('data-authenticated') == "False") {
            $('#error-alert').html("Please <a href='/login'>sign in</a> to purchase a membership").show();
            showLoadingBtn(false);
            return;
        } else if ($('#membership-btn').attr('data-membership') != "None") {
            showLoadingBtn(false);
            $('#error-alert').html("You have already purchased a membership").show();
            return;
        }

        // Handles selection of each membership type
        if ($('#student-info').is(":visible")) {
            var membership_type = 'Student';
            var student_id = $('#student_id').val();
        } else { 
            var membership_type = 'Associate';
        }
     
        // Get Checkout Session ID and redirect to Stripe Checkout
        $.post(
            '/membership',
            {'membership_type' : membership_type, 'student_id' : student_id},
            function(data) {
                
                // Display error message if unsuccessful
                if (data.error) {
                    $('#error-alert').html(data.error).show();
                    showLoadingBtn(false);
                    return;
                } else {
                    $('#error-alert').hide();
                    const stripe = Stripe(data.checkout_public_key);
                    return stripe.redirectToCheckout({ sessionId : data.checkout_session_id })
                }
            }
        );
    });

});
