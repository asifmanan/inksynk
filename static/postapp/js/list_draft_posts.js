$(document).ready(function(){
    list_draft_page_decoration();
});

function list_draft_page_decoration(){
    $("ul.sidebar-nav li a").each(function(){
        $(this).removeClass("link-active");
    });
    $("#id_sidenav_drafts").addClass("link-active");
}