var MENU_SLIDE_DURATION = 110;

$('.dr-one').on('show.bs.dropdown', function() {
if($(window).width() > 767){
    $('.dr-menu-one').first().stop(true, true).slideDown(MENU_SLIDE_DURATION);
}
});

// Add slideUp animation to Bootstrap dropdown when collapsing.
$('.dr-one').on('hide.bs.dropdown', function() {
if($(window).width() > 767){
    $('.dr-menu-one').first().stop(true, true).slideUp(MENU_SLIDE_DURATION);
}
});
$('.dr-two').on('show.bs.dropdown', function() {
if($(window).width() > 767){
    $('.dr-menu-two').first().stop(true, true).slideDown(MENU_SLIDE_DURATION);
}
});

// Add slideUp animation to Bootstrap dropdown when collapsing.
$('.dr-two').on('hide.bs.dropdown', function() {
if($(window).width() > 767){
    $('.dr-menu-two').first().stop(true, true).slideUp(MENU_SLIDE_DURATION);
}
});

$(document).ready(function () {
    $(".navbar-toggle").on("click", function () {
        $(this).toggleClass("active");
    });
});
 function show_detail(){
   document.getElementById('member-type-set').classList.remove("hidden");
   document.getElementById('personal-set').classList.remove("hidden");
   document.getElementById('verification-set').classList.remove("hidden");
 }
 function hide_detail(){
   document.getElementById('member-type-set').classList.add("hidden");
   document.getElementById('personal-set').classList.add("hidden");
   document.getElementById('verification-set').classList.add("hidden");
 }
 function show_home_address(){
   if(document.getElementById('different-address').checked){
      document.getElementById('home-address').classList.remove("hidden");
   } else {
      document.getElementById('home-address').classList.add("hidden");
   }
 }
 function HandleBrowseClick(){
   var fileinput = document.getElementById("browse");
   fileinput.click(); 
 }
 function Handlechange(event){
   var fileinput = document.getElementById("browse");
   var textinput = document.getElementById("filename");
   textinput.value = fileinput.value;
   var selectedFile = event.target.files[0];
   var reader = new FileReader();

   var imgtag = document.getElementById("ava");
   imgtag.title = selectedFile.name;

   reader.onload = function(event) {
   imgtag.src = event.target.result;
   };

   reader.readAsDataURL(selectedFile);
  }