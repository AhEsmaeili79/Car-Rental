// start control outed tab content
$(document).ready(function () {
    $(".nav-pills .nav-link").click(function () {
        let navLinkId = $(this).attr("id");
        $(".contentForTab").css("display", "none");
        $(".contentForTab[for*='" + navLinkId + "']").css("display", "block");
    });
});
// end control outed tab content

$(document).ready(function () {

    /* remove pre loading section */
    $('#preloader').delay(350).fadeOut('slow');
    /* remove pre loading section */

    fixedMenu();
});

// init bootstrap select picker

$(function () {
    $('.selectpicker').selectpicker();
})

// init bootstrap select picker

// start handle circle progress bar

$(function () {

    $(".progress.circle").each(function () {

        var value = $(this).attr('data-value');
        var left = $(this).find('.progress-left .progress-bar');
        var right = $(this).find('.progress-right .progress-bar');

        if (value > 0) {
            if (value <= 50) {
                right.css('transform', 'rotate(' + percentageToDegrees(value) + 'deg)')
            } else {
                right.css('transform', 'rotate(180deg)')
                left.css('transform', 'rotate(' + percentageToDegrees(value - 50) + 'deg)')
            }
        }

    })

    function percentageToDegrees(percentage) {

        return percentage / 100 * 360

    }

});

// end handle circle progress bar

$(window).scroll(function () {
    fixedMenu();
});

// init light gallery
$(function () {
    $('.lightgallery').lightGallery({
        videojs: true
    });
});
// init light gallery

// start comment form validate
$(function () {
    $("#commentForm").validate({
        rules: {
            name: {
                required: true,
                minlength: 8
            },
            family: {
                required: true,
                minlength: 8
            },
            email: {
                required: true,
                email: true
            },
            mobile: {
                required: true,
                minlength: 8
            }
        },
        messages: {
            name: {
                required: "نام خود را وارد نمایید",
                minlength: "نام عبور باید حداقل 2 کاراکتر داشته باشد"
            },
            family: {
                required: "نام خانوادگی خود را وارد نمایید",
                minlength: "رمز عبور باید حداقل 2 کاراکتر داشته باشد"
            },
            email: {
                required: "ایمیل خود را وارد نمایید",
                email: "لطفا یک ایمیل معتبر وارد کنید"
            },
            mobile: {
                required: "موبایل خود را وارد نمایید",
                minlength: "موبایل باید حداقل 11 کاراکتر داشته باشد"
            }
        },
        submitHandler: function (form) {
            form.submit();
        }
    });
})
// end comment form validate

// start control navbar fixed
function fixedMenu() {
    if ($(window).scrollTop() > 70) {
        $(".header-nav").addClass("menu-fixed");
    } else {
        $(".header-nav").removeClass("menu-fixed");
    };
}
// end control navbar fixed

// like button controll class
$(function () {
    $(".like-button").click(function () {
        $(this).toggleClass('liked');
    })

})
// like button controll class


$(function () {
    /*start 4-col-owl carousel*/
    $('.4-col-owl').owlCarousel({
        loop: true,
        rtl: true,
        margin: 10,
        autoWidth: false,
        nav: true,
        dots: false,
        autoplay: true,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1
            },
            620: {
                items: 2
            },
            940: {
                items: 3
            },
            1280: {
                items: 4
            }
        }
    });
    /*end 4-col-carousel*/
})