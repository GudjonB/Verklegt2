var navbar;
var sticky;
var bodyblock;
var confirmationButton;
var cartItems;


// allir takkar sem notaðir eru ekki með jquery sóttir
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

// toggle fyrir burger takkann skiptir um icon og fellir niður auka valmöguleika
// ásam smá bootstrap glimmeri með animation
$(document).ready(function () {
    $('.second-button').on('click', function () {

        $('.animated-icon2').toggleClass('open');
        $("#home-button").toggle();
    });
});


// toggle fyrir profile takkann skiptir um icon og fellir niður auka valmöguleika
$(document).ready(function () {
    $('.profile-button').on('click', function () {
        $(".profIcon").toggleClass("fa-user  fa-user-alt-slash");
        $(".fa-shopping-cart").toggle();
    });
});


// sticky klasanum er bætt við navbarinn þegar búið er að skruna frammhjá bannernum
// til að það myndist ekki stökk á body síðunni þá er bætt við hana top padding sem er jafn þykkur og navbarinn
// ef það er skrunað og pageYofsett er minna en bannerinn þá er sticky tekinn af
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

// pop up alert í endann á kaupum
function purchaseConfirmed() {
    alert("Congratulations with your new property!");
}

