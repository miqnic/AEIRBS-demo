$("#editProfileButton").click(function() {
  $(".editProfileContainer").show();
  $(".userProfile").hide();
});

$("#cancelEditProfile").click(function() {
  $(".editProfileContainer").hide();
  $(".userProfile").show();
});