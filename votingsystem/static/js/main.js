"use strict";
jQuery(document).on('ready', function() {
var slBannerOwl = document.getElementById('slBannerOwl')
if (slBannerOwl !== null) {
    $('#slBannerOwl').owlCarousel({
        loop:true,
        autoplay:true,
        dots:false,
        items:1,
        autoplayTimeout: 5500,
        autoplaySpeed: 2000,
        animateIn: 'fadeIn',
        animateOut: 'fadeOut'
    })
}
var slCategoryOwl = jQuery('#slCategoryOwl');
//on initialize
slCategoryOwl.on('initialized.owl.carousel', function(e) {
  var _this   = jQuery(this);
  _this.find('.owl-item').removeClass('sl-owl');
  _this.find('.owl-item.active').first().addClass('sl-owl');
  _this.find('.owl-item.active').last().addClass('sl-owl');
  // _this.find('.owl-item.active').last().prev('.owl-item.active').addClass('sl-owl');
});

if (slCategoryOwl !== null) {
    $('#slCategoryOwl').owlCarousel({
        loop:true,
        autoplay:true,
        mouseDrag:false,
        nav:true,
        dots:false,
        margin: 30,
        items:6,
        autoplayTimeout: 55000,
        autoplaySpeed: 2000,
        responsive:{
            0:{
                items:1,
            },
            721:{
                items:2,
            },
            991:{
                items:3,
            },
            1200:{
                items:4,
            },
            1440:{
                items:5,
            },
            1750:{
                items:6
            }
        }
    });
    //on change
    slCategoryOwl.on('changed.owl.carousel', function(e) {
      var _this   = jQuery(this);
      _this.find('.owl-item').removeClass('sl-owl');
      setTimeout(function(){
        _this.find('.active').first().addClass('sl-owl');
        _this.find('.active').last().addClass('sl-owl');
      }, 10);
    });
    $("#slCategoryOwl .owl-prev").html('<i class="ti-arrow-left"></i>')
    $("#slCategoryOwl .owl-next").html('<i class="ti-arrow-right"></i>')
}
var slFeedbackOwl = document.getElementById('slFeedbackOwl')
if (slFeedbackOwl !== null) {
    $(slFeedbackOwl).owlCarousel({
        loop:true,
        autoplay:true,
        nav:false,
        dots:false,
        margin: 30,
        items:2,
        autoplayTimeout: 5500,
        autoplaySpeed: 2000,
        responsive:{
            0:{
                items:1,
            },
            1200:{
                items:2,
            }
        }
    })
}
var slVendorSingleOwl = document.getElementById('slVendorSingleOwl')
if (slVendorSingleOwl !== null) {
    $(slVendorSingleOwl).owlCarousel({
        loop:true,
        autoplay:true,
        nav:false,
        dots:false,
        items:1,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
    })
}
var slProductProviderOwl = document.getElementById('slProductProviderOwl')
if (slProductProviderOwl !== null) {
    $(slProductProviderOwl).owlCarousel({
        loop:false,
        autoplay:false,
        nav:false,
        dots:true,
        items:1,
        autoplayTimeout: 5500,
        autoplaySpeed: 2000,
    })
}
var serviceProviderSingleBanner = document.getElementById('serviceProviderSingleBanner')
if (serviceProviderSingleBanner !== null) {
    $(serviceProviderSingleBanner).owlCarousel({
      loop:true,
      autoplay:true,
      rewind: true,
      nav:true,
      dots:false,
      items:3,
      autoplayHoverPause:true,
      autoplayTimeout: 5500,
      autoplaySpeed: 2000,
      responsive:{0:{items:1,},421:{items:2,},768:{items:3,}
    }
  })
  $("#serviceProviderSingleBanner .owl-prev").html('<i class="ti-arrow-left"></i>')
  $("#serviceProviderSingleBanner .owl-next").html('<i class="ti-arrow-right"></i>')
}
var syncOwl = document.getElementById('sl-sync1')
if (syncOwl !== null) {
  function product(){
    var sync1 = jQuery('#sl-sync1');
    var sync2 = jQuery('#sl-sync2');
    var slidesPerPage = 3;
    var syncedSecondary = true;
    sync1.owlCarousel({
      items : 1,
      loop: true,
      nav: false,
      dots: false,
      autoplay: false,
      video:true,
      Height: 370,
      lazyLoad: true,
      slideSpeed : 2000,
      responsiveRefreshRate : 200,
    }).on('changed.owl.carousel', syncPosition);
    sync2.on('initialized.owl.carousel', function () {
      sync2.find(".owl-item").eq(0).addClass("current");
    })
    .owlCarousel({
      // items : slidesPerPage,
      items:6,
      dots: false,
      nav: false,
      margin:10,
      smartSpeed: 200,
      slideSpeed : 500,
      slideBy: slidesPerPage,
      responsiveRefreshRate : 100,
    }).on('changed.owl.carousel', syncPosition2);
    function syncPosition(el) {
      var count = el.item.count-1;
      var current = Math.round(el.item.index - (el.item.count/2) - .5);
      if(current < 0) {
        current = count;
      }
      if(current > count) {
        current = 0;
      }
      sync2
      .find(".owl-item")
      .removeClass("current")
      .eq(current)
      .addClass("current")
      var onscreen = sync2.find('.owl-item.active').length - 1;
      var start = sync2.find('.owl-item.active').first().index();
      var end = sync2.find('.owl-item.active').last().index();
      if (current > end) {
        sync2.data('owl.carousel').to(current, 100, true);
      }
      if (current < start) {
        sync2.data('owl.carousel').to(current - onscreen, 100, true);
      }
    }
    function syncPosition2(el) {
      if(syncedSecondary) {
        var number = el.item.index;
        sync1.data('owl.carousel').to(number, 100, true);
      }
    }
    sync2.on("click", ".owl-item", function(e){
      e.preventDefault();
      var number = jQuery(this).index();
      sync1.data('owl.carousel').to(number, 300, true);
    });
  }
  product();
}

var slInputIncrement = document.querySelector('.sl-input-increment')
if (slInputIncrement !== null) {
  jQuery(document).on('click','.sl-input-increment',function(e) {
      var $input = $(this).closest('.sl-vlaue-btn').find('.sl-input-number');
      var val = parseInt($input.val(), 10);
      $input.val(val + 1);
  })
  jQuery(document).on('click','.sl-input-decrement',function(e) {
      var $input = $(this).closest('.sl-vlaue-btn').find('.sl-input-number');
      var val = parseInt($input.val(), 10);
      if (val >= 1) {
          $input.val(val - 1);
      }
  })
}
var slCartDelete = document.querySelector('.sl-cart-delete')
if (slCartDelete !== null) {
  jQuery(document).on('click','.sl-cart-delete',function(e) {
      $(this).closest('li').remove();
  })
}
var slDropdown__cart = document.querySelector('.sl-dropdown__cart')
if (slDropdown__cart !== null) {
  jQuery(document).on('click','.sl-dropdown__cart',function(e) {
      e.stopPropagation();
  })
}
var dropdown_notify = document.querySelector('.sl-dropdown__notify')
if (dropdown_notify !== null) {
  jQuery(document).on('click','.sl-dropdown__notify',function(e) {
    e.stopPropagation();
  })
}
/* MAIN HEADER LOCATION DISTANCE START*/
var slArrowIcon = document.querySelector('.sl-arrow-icon')
if (slArrowIcon !== null) {
  $('.sl-arrow-icon').on('click',function(){
      $(this).siblings('.sl-distance').slideToggle( "fast" );
   })
}
  /* MAIN HEADER LOCATION DISTANCE END*/
  var slShareHolder = document.querySelector('.slShareHolder')
  if (slShareHolder !== null) {
    jQuery(document).on('click','.slShareHolder',function(e){
      var _this = jQuery(this);
      if( _this.next('.sl-shareHolder__option').hasClass('sl-shareHolder--animatein') ){
        _this.next('.sl-shareHolder__option').addClass('sl-shareHolder--animateout');
        setTimeout(function(){
          _this.next('.sl-shareHolder__option').removeClass('sl-shareHolder--animateout sl-shareHolder--animatein');
        }, 550);
      } else{
        _this.next('.sl-shareHolder__option').toggleClass('sl-shareHolder--animatein');
      }
    });
  }

/* SLIDER RANGE MIN START */
var sliderRangeMin = document.getElementById('slider-range-min')
if (sliderRangeMin !== null) {
  $( function() {
    $( "#slider-range-min" ).slider({
      range: "min",
      value: 70,
      min: 1,
      max: 700,
      slide: function( event, ui ) {
        $( "#amountfour" ).val(ui.value + " km");
      }
    });
    $( "#amountfour" ).val($( "#slider-range-min" ).slider( "value" ) + " km" );
  } );
}
var sliderRange = document.getElementById('slider-range')
if (sliderRange !== null) {
  $( function() {
		$( "#slider-range" ).slider({
		  range: true,
		  min: 0,
		  max: 2000,
		  values: [ 450, 1600 ],
		  slide: function( event, ui ) {
			$( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
		  }
		});
		$( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
		  " - $" + $( "#slider-range" ).slider( "values", 1 ) );
	  } );
}
/* SLIDER RANGE MIN END */
var search = document.getElementById('sl-search')
if (search !== null) {
  jQuery(document).on('click', '#sl-search', function(e){
    jQuery(this).closest('body').addClass('sl-sidebar--open');
  });

  jQuery(document).on('click', '#sl-close', function(e){
    jQuery(this).closest('body').addClass('sl-sidebar--animate');
    $(this).delay(650).queue(function() {
      jQuery(this).closest('body').removeClass('sl-sidebar--open');
      jQuery(this).closest('body').removeClass('sl-sidebar--animate');
      $(this).dequeue();
   });
  })
  
}
//  PRETTY PHOTO START
var prettyOne = document.querySelector(".sl-prettyPhotoImg")
if (prettyOne !== null) {
  jQuery(".sl-prettyPhotoImg").prettyPhoto({
  animation_speed: 'normal',
  theme: 'dark_square',
  allow_resize: true,
  slideshow: 3000,
  autoplay_slideshow: false,	
  social_tools: false,
  show_title: true
  });
}
var prettyTwo = document.querySelector('.sl-video__img')
if (prettyTwo !== null) {
  jQuery(".sl-video__img").prettyPhoto({
    theme: 'dark_square',
    autoplay: true,
    iframe_markup: "<iframe src='{path}' width='{width}' height='{height}' frameborder='no' allowfullscreen='true'></iframe>"
  });
}
//  PRETTY PHOTO END
// TIPSO TOOLTIP START 
var toltip_content = document.querySelector(".toltip-content")
if (toltip_content !== null) {
  jQuery('.toltip-content').tipso({
      speed             : 400,        
      background        : '#ffca28',
      titleBackground   : '#ffca28',
      color             : '#fff',
      titleColor        : '#ffca28',
      width             : 105,
      tooltipHover      : true,
      size :50,
      offsetY : 0,
      position: 'top-right'
    });
    jQuery('.hover-tipso-tooltip').tipso({
      tooltipHover: true,
  });
}
  // TIPSO TOOLTIP END
  // PROGRESS BAR START
  
  try {
    $('.sl-usersinfo').appear(function () {
      jQuery('.sl-skillholder').each(function () {
        jQuery(this).find('.sl-skillbar').animate({
          width: jQuery(this).attr('data-percent')
        }, 2500);
      });
    });
  } catch (err) {}
  // Dashboard Menu
  function collapseMenuSidebar(){
    jQuery('.sl-navdashboard ul li.menu-item-has-children').on('click', function(){
      jQuery(this).toggleClass('sl-openmenu');
      jQuery(this).find('.sub-menu').slideToggle(300);
    });
  }
  collapseMenuSidebar();
  /* TINYMCE WYSIWYG EDITOR */
  if(jQuery('.sl-tinymceeditor').length > 0){
    tinymce.init({
      selector: 'textarea.sl-tinymceeditor',
      height: 300,
      theme: 'modern',
      plugins: [ 'advlist autolink lists link image charmap print preview hr anchor pagebreak'],
      menubar: false,
      statusbar: false,
      toolbar1: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify',
      image_advtab: true,
    });
  }
  // PROGRESSbAR START
  var progressbar = document.getElementById('progressbar1')
  if (progressbar !== null) {
    $( function() {
      $( "#progressbar1" ).progressbar({
        value: 90
      });
      $( "#progressbar2" ).progressbar({
        value: 70
      });
      $( "#progressbar3" ).progressbar({
        value: 32
      });
      $( "#progressbar4" ).progressbar({
        value: 20
      });
      $( "#progressbar5" ).progressbar({
        value: 5
      });
    } );
  }
  // PROGRESSbAR END
    // DHB USER LOGO START
    jQuery(document).on('click', '#collapseUser a', function(e){
      e.preventDefault();
      var usertext = jQuery(this).find('em').text();
      var circlecolor = jQuery(this).find('span').attr('class');
  
      jQuery('.sl-userStatus__content > a:first-child > span + em').html(usertext)
      jQuery('.sl-userStatus__content > a:first-child > span em').removeClass().addClass(circlecolor);
      $('#collapseUser').collapse('toggle');
    });
    // DHB USER LOGO END
    // SELLECT 2 START
	$('#sl-intervals').select2({
    placeholder: "Intervals",
    minimumResultsForSearch: Infinity
  });
	$('#sl-appointment-duration').select2({
    placeholder: "Appointment Duration",
    minimumResultsForSearch: Infinity
  });
	$('#sl-languages').select2({
    placeholder: "Select Language(s)",
    allowClear: true
  });
	$('#sl-ameneties').select2({
    placeholder: "Select Ameneties & Features",
    allowClear: true
  });
	$('#sl-articleTitle').select2({
    placeholder: "Article Title",
    allowClear: true
  });
	$('#sl-chooseCategory').select2({
    placeholder: "Choose Category",
    allowClear: true
  });
	$('#sl-chooseTag').select2({
    placeholder: "Choose Tag",
    allowClear: true
  });
  $('#sl-selectservice').select2({
    placeholder: "Select Service(s)*",
    allowClear: true
  });
  // SELLECT 2 END
  // GOOGLE MAP START
	if(jQuery('#sl-locationmap').length > 0){
    var center = [37.772323, -122.214897];
    $('#sl-locationmap')
    .gmap3({
        center: center,
        zoom: 13,
        mapTypeId : google.maps.MapTypeId.ROADMAP
    })
    .marker({
        position: center,
        icon: 'https://maps.google.com/mapfiles/marker_green.png'
    });
  }
  // GOOGLE MAP END
  // DATEPICKER START 
	var datepicker = document.querySelector('.datepicker')
	if (datepicker !== null) {
	  $('.datepicker').datepicker({
		format: 'mm/dd/yyyy',
		startDate: '-3d'
	  });
	}
  // DATEPICKER END
  // LINKIFY START
	var link = document.querySelector('.sl-messageUser__area')
	if (link !== null) {
	  $('.sl-messageUser__area p').linkify();
	  $('#sidebar').linkify({
		  target: "_blank"
	  });
	}
  // LINKIFY END
  jQuery('.sl-selectAll1').click(function() {
    jQuery(this).closest('.sl-checkbox').next('ul').find('input').not(this).prop('checked', this.checked);
  });
  jQuery('.sl-selectAll2').click(function() {
    jQuery(this).closest('li').siblings('li').find('input').not(this).prop('checked', this.checked);
  });
	/* ADD AND REMOVE CLASS START */
	$('.sl-main-form__btn').on('click', function(){
	  $('.sl-main-header__upper').addClass('sl-navbar-search')
	})
	$('.sl-main-upperBackbtn').on('click', function(){
	  $('.sl-main-header__upper').removeClass('sl-navbar-search')
	})
	$('.sl-main-header__lower--btn').on('click', function(){
	  $('.sl-main-header__lower').addClass('sl-more-info')
	})
	$('.sl-main-lowerBackbtn').on('click', function(){
	  $('.sl-main-header__lower').removeClass('sl-more-info')
	})
  /* ADD AND REMOVE CLASS END */
  jQuery(document).on('click', '#sl-closeasidebar', function(e){
    jQuery('#sl-asidebar').toggleClass('sl-asideshow')
    jQuery('body').toggleClass('sl-scrollY-none')
    jQuery(this).find('i').toggleClass('lnr lnr-layers lnr lnr-cross')
  })
  //  COMINGSOON COUNTER
  var search = document.getElementById('sl-cscounter')
  if (search !== null) {
    jQuery('#sl-cscounter').countdown('2021/02/05', function(event) {
          var $this = jQuery(this).html(event.strftime(''
              + '<div class="sl-cscounter__holder"><div class="sl-cscounter__countdown"><h4>%-D</h4><span>days</span></div></div>'
              + '<div class="sl-cscounter__holder"><div class="sl-cscounter__countdown"><h4>%H</h4><span>hours</span></div></div>'
              + '<div class="sl-cscounter__holder"><div class="sl-cscounter__countdown"><h4>%M</h4><span>Minutes</span></div></div>'
              + '<div class="sl-cscounter__holder"><div class="sl-cscounter__countdown"><h4>%S</h4><span>Seconds</span></div></div>'
          ));
      });
  }
  var search = document.getElementById('sl-packagecounter')
  if (search !== null) {
    jQuery('#sl-packagecounter').countdown('2021/02/05', function(event) {
          var $this = jQuery(this).html(event.strftime(''
              + '<li><div class="sl-buyPackage__heading"><h3>%-D</h3><h6>Days</h6></div></li>'
              + '<li><div class="sl-buyPackage__heading"><h3>%H</h3><h6>Hours</h6></div></li>'
              + '<li><div class="sl-buyPackage__heading"><h3>%M</h3><h6>Minutes</h6></div></li>'
              + '<li><div class="sl-buyPackage__heading"><h3>%S</h3><h6>Seconds</h6></div></li>'
          ));
      });
  }
  jQuery(document).on('click', '.sl-inbox__user--list li', function(){
		jQuery('.sl-dashboardbox__content').addClass('sl-message-js')
	  });
	  jQuery(document).on('click', '.sl-messageUser__back', function(){
		jQuery('.sl-dashboardbox__content').removeClass('sl-message-js')
    });
    /* MOBILE MENU*/
       function collapseMenu(){
            if ($(window).width() < 992) {
              jQuery('.sl-main-header .navbar-collapse .sl-navbar-nav li.sl-dropdown a, .sl-main-header .navbar-collapse .sl-navbar-nav li.menu-item-has-mega-menu a').on('click', function() {
              jQuery(this).parent('li').toggleClass('sl-open-menu');
              jQuery(this).next().slideToggle(300);
            });
          }
      }
      collapseMenu();
    /* MOBILE MENU*/
    jQuery(document).on('click','#sl-appointmentPopupbtn1',function(e){
      jQuery(this).closest('.modal-content').addClass('sl-appointmentPopup__1 sl-appointmentPopup-footer')
    })
    jQuery(document).on('click','#sl-appointmentPopupbtn2',function(e){
      jQuery(this).closest('.modal-content').removeClass('sl-appointmentPopup__1').addClass('sl-appointmentPopup__2')
    })
    jQuery(document).on('click','#sl-appointmentPopupbtn3',function(e){
      jQuery(this).closest('.modal-content').removeClass('sl-appointmentPopup__2').addClass('sl-appointmentPopup__3')
    })
    jQuery(document).on('click','.modal-header .close',function(e){
      jQuery(this).closest('.modal-content').removeClass('sl-appointmentPopup__1 sl-appointmentPopup__2 sl-appointmentPopup__3 sl-appointmentPopup-footer')
    })
    	/* PRELOADER*/
	jQuery(window).on('load', function() {
    jQuery(".preloader-outer").delay(600).fadeOut();
	});

  /*  APPOINTMENTS CALENDER  */
  var slCalendar = document.getElementById('sl-calendar')
  if (slCalendar !== null) {
    jQuery('#sl-calendar').fullCalendar({
      height: 'auto',
      dayClick: function(date, jsEvent, view) {
        alert('Clicked on: ' + date.format());
      }
    });
    $(".sl-appointmentPopup").on('shown.bs.modal', function () {
        $("#sl-calendar").fullCalendar('render');
     });
  }
      /* COUNTER */
	try {
		var _wt_statistics = jQuery('#counter');
		_wt_statistics.appear(function () {
			var _wt_statistics = jQuery('.sl-stats__description h3');
			_wt_statistics.countTo({
				formatter: function (value, options) {
					return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
				}
			});
		});
  } catch (err) {}
});
