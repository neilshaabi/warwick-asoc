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
            700: {
                slidesPerView: 2
            },
            1150: {
                slidesPerView: 3
            }
        }
    });

});