$(document).ready(function(){
    categories_home_page_decoration();
});

function categories_home_page_decoration(){
    $("ul.sidebar-nav li a").each(function(){
        if ($(this).hasClass("link-active")){
            $(this).removeClass("link-active");
        }
    });
    $("#id_sidenav_categories").addClass("link-active");
}