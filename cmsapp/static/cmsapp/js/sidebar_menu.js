$("#menu-toggle").click(function(e) {
  e.preventDefault();
  $("#wrapper").toggleClass("toggled");
});

$(".sidenav-btn-collapse").click(function(e) {
 e.preventDefault();
 this.blur();
  if (!$(this).next(".sidebar-collapse-menu").hasClass("show")) {
      $(".selected").css("height","0px")
      $(".sidebar-collapse-menu").each(function(){
        $(".sidebar-collapse-menu").removeClass("selected show");
      })
      $(this).next(".sidebar-collapse-menu").addClass("selected")
      var sublink_items = $("div.selected a").length;
      div_height = 40*sublink_items;
      div_height_px = div_height.toString()+"px";
      console.log(div_height_px);
      $(".selected").css("height",div_height_px);
      $(this).next(".sidebar-collapse-menu").addClass("show");
  }
  else {
      $(".selected").css("height","0px");
      $(this).next(".sidebar-collapse-menu").removeClass("selected show");
  }
});

$(document).on("click","#id--toggle-table-view", function(e){
e.preventDefault();
$(".description--field").toggleClass("compressed");
})