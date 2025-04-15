
document.addEventListener("DOMContentLoaded", function () {
  if (document.querySelector('.swiper-1')){
    const swiper1 = new Swiper('.swiper-1', {
      loop: true,
      autoplay: {
        delay: 3000,  // slide per 3sec
        disableOnInteraction: false, // auto play after user action
    },
      // If we need pagination
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
        
      },
      slidesPerView: 1, 
      });
  }

  if (document.querySelector('.swiper-2')){
    const swiper2 = new Swiper('.swiper-2', {
      loop: false,
      autoplay: {
        delay: 3000,
        disableOnInteraction: false,
    },
      // If we need pagination
      pagination: {
        el: '.swiper-pagination-2',
        clickable: true,
      },
      slidesPerView: 1, // mobile size
      breakpoints:{
            768:{
              slidesPerView: 3,//for tablet and desktop
              spaceBetween: 30,
            }
          },
          navigation: window.innerWidth >= 768 ? { // タブレット以上のみ適用
            nextEl: ".next",
            prevEl: ".prev"
        } : false
      });
  }

  if (document.querySelector('.swiper-3')){
    const swiper3 = new Swiper('.swiper-3', {
      loop: false,
      autoplay: false,
      // If we need pagination
      pagination: {
        el: '.swiper-pagination-3',
        clickable: true,
      },
      slidesPerView: 1, // mobile size
          navigation: { 
            nextEl: ".next-3",
            prevEl: ".prev-3"
        }
      });
  }

  if (document.querySelector('.swiper-4')){
    if (document.querySelector('.swiper-4')){

    const swiper4 = new Swiper('.swiper-4', {
      loop: false,
      autoplay: false,
      // If we need pagination
      pagination: {
        el: '.swiper-pagination-4',
        clickable: true,
      },
      slidesPerView: 1, // mobile size
          navigation: { 
            nextEl: ".next-4",
            prevEl: ".prev-4"
        }
      });
  }
  }
});
