
$(document).ready(function() {	
	// MENU MOBILE //
	$(".wrapMenuMobile").click(function() {
		$(this).toggleClass('active');
		$(".menuMobile").toggleClass('active');
		$(".menu ul").fadeToggle();
		$(".sub").css('display','none');
		$(".menu li i").removeClass('active');
	});	
	
	// SCROLL //
	$(".scroll").click(function() {
		var c = $(this).attr("href");
		$('html, body').animate({ scrollTop: $("#" + c).offset().top }, 1000, "linear");
		return false;
	});

	$('#slidepart').slick({
		dots: false,
		infinite: true,
		autoplaySpeed: 4000,
		speed: 1000,
		slidesToShow: 6,
		slidesToScroll: 1,
		arrows: false,
		autoplay: true,
		pauseOnHover: false,
		responsive: [{
				breakpoint: 1235,
				settings: {
					slidesToShow: 5,
				}
			},
			{
				breakpoint: 1053,
				settings: {
					slidesToShow: 4,
				}
			},
			{
				breakpoint: 768,
				settings: {
					slidesToShow: 3,
				}
			},
			{
				breakpoint: 610,
				settings: {
					slidesToShow: 2,
				}
			},

			{
				breakpoint: 481,
				settings: {
					slidesToShow: 2,
					fade:true
				}
			},
		]
	});



	
});

