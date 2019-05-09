var navbar;
var sticky;
var bodyblock;

$(document).ready(function(){
  // Get the navbar
  navbar = document.getElementById("navbar");
  // Get the offset position of the navbar
  sticky = navbar.offsetTop;
  var width = navbar.offsetWidth;
  // Get Bodyblock
  bodyblock = document.getElementsByClassName("bodyBlock")[0];
});


$(document).ready(function () {
  $('.second-button').on('click', function () {

    $('.animated-icon2').toggleClass('open');
  });
});

$(document).ready(function () {
  $('.profile-button').on('click', function () {
    $(".profIcon").toggleClass("fa-user  fa-user-alt-slash");
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