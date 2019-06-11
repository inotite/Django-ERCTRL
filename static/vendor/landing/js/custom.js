	
$( document ).ready(function() {
	
"use strict";

    $('.owl-one').owlCarousel({
    loop:true,
    margin:10,
    nav:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:3
        },
        1000:{
            items:5
        }
    }
});




});

$('.owl-carousel').owlCarousel({
    items:1,
	loop:true,
    nav:true,
	dots:true,
	autoplay:true,
	navText:["<i class='fa fa-angle-left' aria-hidden='true'></i>","<i class='fa fa-angle-right' aria-hidden='true'></i>"]
    
})

$(window).scroll(function(){
  var sticky = $('.navbar'),
      scroll = $(window).scrollTop();

  if (scroll >= 100) sticky.addClass('nav_fix');
  else sticky.removeClass('nav_fix');
});









