
$(document).ready(function(){

    // Toggle active state for navbar link when selected
    var pathname = window.location.pathname;
    var links = document.getElementsByClassName('nav-link');
    for (var i = 0; i < links.length; i++) {
        if (pathname == links[i].getAttribute('href')) {
            links[i].classList.add('active');
            break;
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
            
            // Redirect to home page if successful
            else {
                window.location = data;
            }
        });
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
        });
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

    
    // Membership selection handler using AJAX
    $('#membership-form').on('submit', function(event) {

        event.preventDefault();
        showLoadingBtn(true);
        $('#error-alert').hide();
        
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

        // Handles student membership selection
        if ($('#student-info').is(":visible")) {
            
            var membership_type = 'Student';

            // Validate student ID
            // var student_id = Number($('#student_id').val());
            // if ((student_id < 1000000) || (student_id > 2200000)
            //     || !(Number.isInteger(student_id))) {
            //     $('#error-alert').html("Invalid student ID").show();
            //     return;
            // } else {    
            //     $('#error-alert').hide();
            // }

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
                    return;
                } else {
                    const stripe = Stripe(data.checkout_public_key);
                    return stripe.redirectToCheckout({ sessionId : data.checkout_session_id })
                }
            }
        );
    });


    // Team page swiper
    const teamSwiper = new Swiper('.team-swiper', {
        
        direction: 'horizontal',
        grabCursor: 'true',
        spaceBetween: 20,
        slidesPerView: 3,
        loop: true,

        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
    
        pagination: {
            el: '.swiper-pagination',
            dynamicBullets: true,
            clickable: true,
        },

        breakpoints: {
            0: {
                slidesPerView: 1
            },
            850: {
                slidesPerView: 2
            },
            1150: {
                slidesPerView: 3
            }
        }
    });


    function showLoadingBtn(loading) {
        if (loading == true) {
            $(':input[type="submit"]').prop('disabled', true);
            $('.btn-text').hide();
            $('.spinner-border').show();
        } else {
            $(':input[type="submit"]').prop('disabled', false);
            $('.btn-text').show();
            $('.spinner-border').hide();
        }
    }

});
