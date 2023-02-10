$(document).ready(function(){
    list_published_page_decoration();
});

function list_published_page_decoration(){
    $("ul.sidebar-nav li a").each(function(){
        $(this).removeClass("link-active");
    });
    $("#id_sidenav_published").addClass("link-active");
}