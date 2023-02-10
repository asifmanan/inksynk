$(document).ready(function(){
  new_post_page_decoration();
  $('body').on('submit','#id_post_form',function(event){
    event.preventDefault()
    main_func();
  });
  $('body').on('submit','#id_modal_login_form',function(event){
    event.preventDefault()
    user_auth();
  });
});

//form validation is handled by bootstrap "bs_form_validator.js"

function new_post_page_decoration(){
  $("#id_sidenav_newpost").addClass('link-active');
  $("#id_sidenav_published").removeClass('link-active');
}

function main_func(){
  const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
  var url = $('#id_loginstatusquery').attr("loginstatusquery_url");
  loginstatusquery(submit_post,csrftoken,url);
}

function submit_post(csrf_token){
    const csrftoken = csrf_token;
    var url = $('#id_post_content_url').attr("post_save_url")
    var title = $("#id_title").val();
    var summary = $("#id_summary").val();
    var content = $("#id_content").val();
    $.ajax({
      url:url,type:"POST",
      headers:{'X-CSRFToken':csrftoken},
      datatype:'json',
      data:{
        'title':title,
        'summary':summary,
        'content':content,
      },
      success: function(data){
        $('#id_title').val(data['title']);
        $('#id_title').attr('disabled',true);
        $('#id_summary').val(data['summary']);
        $('#id_summary').attr('disabled',true);
        $('#id_content').val(data['content']);
        $('#id_content').attr('disabled',true);
        $('#id_post_save').attr('disabled',true);
        }
      }

    )
}
