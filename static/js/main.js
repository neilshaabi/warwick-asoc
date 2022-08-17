
$(document).ready(function(){

    // Toggle active state for navbar link when selected
    var pathname = window.location.pathname;
    var links = document.getElementsByTagName('a');
    for (var i = 0; i < links.length; i++) {
        if (pathname == links[i].getAttribute('href')) {
            links[i].classList.add('active');
            break;
        }
    }

    // Zoom effect for hero image
    $(window).scroll(function() {
        var scroll = $(window).scrollTop();
        $(".hero-img").css({
        backgroundSize: (100 + scroll/10)  + "%",
        top: -(scroll/10)  + "%",
            });
        });


    // Registration handler using AJAX
    $('#register-form').on('submit', function(event) {

        $.post(
            '/register', 
            {'first_name' : $('#first_name').val(), 'last_name' : $('#last_name').val(), 
             'email' : $('#email').val(), 'password' : $('#password').val()}, 
            function(data) {
            
            // Display error message if unsuccessful
            if (data.error) {
                 $('#error-alert').html(data.error).show();
            } 
            
            // Redirect to home page if successful
            else {
                window.location = data;
            }
        });
        event.preventDefault();
    });
    

    // Login handler using AJAX
    $('#login-form').on('submit', function(event) {

        $.post(
            '/login', 
            {'email' : $('#email').val(), 'password' : $('#password').val()}, 
            function(data) {
            
            // Display error message if unsuccessful
            if (data.error) {
                 $('#error-alert').html(data.error).show();
            } 
            
            // Redirect to home page if successful
            else {
                window.location = data;
            }
        });
        event.preventDefault();
    });


    // Password reset request handler using AJAX
    $('#reset-request-form').on('submit', function(event) {

        $.post(
            '/reset-password', 
            {'form-type' : 'request', 'email' : $('#email').val()}, 
            function(data) {
            
            // Display error message if unsuccessful
            if (data.error) {
                 $('#error-alert').html(data.error).show();
            } 
            
            // Redirect to home page if successful
            else {
                window.location = data;
            }
        });
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
        });
        event.preventDefault();
    });


    // Profile edits handler using AJAX
    $('#profile-form').on('submit', function(event) {

        // Get student ID if it exists
        var student_id = null;
        if ($('#membership').val() == 'Student') {
            student_id = $('#student_id').val();
        }

        $.post(
            '/profile', 
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
        });
        event.preventDefault();
    });


    // Toggle between viewing student and associate membership info
    $('.membership-toggles').on('click', function(event) {
        
        // Hide both sections initially
        $('.membership-info').hide();

        // Hide error message
        $('#error-alert').hide();

        // Show section whose id contains the
        var id = (event.target.id).split('-')[0];
        $(".membership-info[id^='" + id + "']").show();

        $('.toggle').removeClass('active-toggle');
        $(event.target).addClass('active-toggle');
    });

    
    // Handles membership selection
    $('#select-membership-btn').on('click', function(event) {
        
        // Displays error message if user is not logged in or already a member
        if ($(event.target).attr('data-authenticated') == "False") {
            $('#error-alert').html("Please <a href='/login'>sign in</a> to purchase a membership").show();
            return;
        } else if ($(event.target).attr('data-membership') != "None") {
            $('#error-alert').html("You have already purchased a membership").show();
            return;
        }

        // Handles student membership selection
        if ($('#student-info').is(":visible")) {
            
            var membership_type = 'Student';

            // Validate student ID
            var student_id = Number($('#student_id').val());
            if ((student_id < 1000000) || (student_id > 2200000)) {
                $('#error-alert').html("Invalid student ID").show();
                return;
            } else {    
                $('#error-alert').hide();
            }

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
                    $('#error-alert').html("Error: " + data.error).show();
                    return;
                } else {
                    const stripe = Stripe(data.checkout_public_key);
                    return stripe.redirectToCheckout({ sessionId : data.checkout_session_id })
                }
            }
        );
    });

});
