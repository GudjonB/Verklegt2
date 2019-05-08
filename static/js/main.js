var navbar;
var sticky;
var bodyblock;

$(document).ready(function(){
  // Get the navbar
  navbar = document.getElementById("navbar");
  // Get the offset position of the navbar
  sticky = navbar.offsetTop;
  // Get Bodyblock
  bodyblock = document.getElementsByClassName("bodyBlock")[0];
});


$(document).ready(function () {
  $('.second-button').on('click', function () {

    $('.animated-icon2').toggleClass('open');
  });
});




window.addEventListener("scroll", event => {

      if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky");
        bodyblock.style.paddingTop="100px";
      }
      else {
        navbar.classList.remove("sticky");
        bodyblock.style.paddingTop="";
      }}
);