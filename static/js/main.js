let navbar;
let sticky;
let bodyblock;
let confirmationButton;


$(document).ready(function () {                                              // All elements that will be used without jquery
    navbar = document.getElementById("navbar");                    // Get the navbar
    sticky = navbar.offsetTop;                                              // Get the offset position of the navbar
    bodyblock = document.getElementsByClassName("bodyBlock")[0]; // Get Bodyblock
    confirmationButton = document.getElementById("confirmButton");

});


$(document).ready(function () {                                     // Toggle the burger icon when clicked and collapsing it
    $('.second-button').on('click', function () {     // along with some glitter and animations

        $('.animated-icon2').toggleClass('open');
        $("#home-button").toggle();
    });
});


$(document).ready(function () {                                     // Toggle the profile icon when clicked and collapse it
    $('.profile-button').on('click', function () {
        $(".profIcon").toggleClass("fa-user  fa-user-alt-slash");
        $(".fa-shopping-cart").toggle();
    });
});


window.addEventListener("scroll", event => { // When the page is scrolled further then the width of the banner
        if (window.pageYOffset >= sticky) {                   // the sticky class is added to it so it sticks to the top
            navbar.classList.add("sticky");                   // of the page and follows the user down, when the class is added
            bodyblock.style.paddingTop = "100px";               // 100px the width of the navbar is added to the top padding
        }                                                     // so the page doesn't appear to jump
        else {
            navbar.classList.remove("sticky");
            bodyblock.style.paddingTop = "";

        }
    }
);


function purchaseConfirmed() {                          // pop up alert when a successful purchase has been made
    alert("Congratulations with your new property!");
}

