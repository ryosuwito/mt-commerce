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
 function HandleBrowseClick(id){
   if(id == "btn_ktp"){
      var fileinput = document.getElementById("id_ktp_photo");
   }
   else if(id == "btn_bank"){
      var fileinput = document.getElementById("id_bank_book_photo");
   }
   else if(id == "btn_profile"){
      var fileinput = document.getElementById("id_profile_photo");
   }
   fileinput.click(); 
 }
 function Handlechange(event, id){
    if(id == "id_ktp_photo"){
        var fileinput = document.getElementById("id_ktp_photo");
        var textinput = document.getElementById("ktp_filename");
        var imgtag = document.getElementById("dummy_ktp_photo");
        $('#btn_ktp').css('display', 'none');
    }
    else if(id == "id_bank_book_photo"){
        var fileinput = document.getElementById("id_bank_book_photo");
        var textinput = document.getElementById("bank_book_filename");
        var imgtag = document.getElementById("dummy_bank_book_photo");
        $('#btn_bank').css('display', 'none');
    }
    else if(id == "id_profile_photo"){
        var fileinput = document.getElementById("id_profile_photo");
        var textinput = document.getElementById("profile_photo_filename");
        var imgtag = document.getElementById("dummy_profile_photo");
        $('#btn_profile').css('display', 'none');
    }
   textinput.value = fileinput.value.replace("C:\\fakepath\\","");
   var selectedFile = event.target.files[0];
   var reader = new FileReader();

   imgtag.title = selectedFile.name;

   reader.onload = function(event) {
   imgtag.src = event.target.result;
   };

   reader.readAsDataURL(selectedFile);
  }