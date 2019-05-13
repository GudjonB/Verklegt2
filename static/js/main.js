var navbar;
var sticky;
var bodyblock;
var confirmationButton;
var cartItems;

$(document).ready(function(){
  // Get the navbar
  navbar = document.getElementById("navbar");
  // Get the offset position of the navbar
  sticky = navbar.offsetTop;
  var width = navbar.offsetWidth;
  // Get Bodyblock
  bodyblock = document.getElementsByClassName("bodyBlock")[0];
  confirmationButton = document.getElementById("confirmButton");
});


$(document).ready(function () {
  $('.second-button').on('click', function () {

    $('.animated-icon2').toggleClass('open');
  });
});

$(document).ready(function () {
  $('.profile-button').on('click', function () {
    $(".profIcon").toggleClass("fa-user  fa-user-alt-slash");
    $(".fa-shopping-cart").toggle();
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

function purchaseConfirmed() {
    alert("Congratulations with your new property!");
}