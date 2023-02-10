$(document).ready(function(){
  $('body').on('click','#id_post_save',function(event){
    event.preventDefault()
    main_func();
  });
  $('.post_required').on('input',post_rem_invalid);
});

function main_func(){
  var form_is_valid = check_post_form_valid();
  if (form_is_valid){
    loginstatuscheck();
    }
  else {
    post_form_add_invalid();
  }
}

function loginstatuscheck(){
  var status = false;
  const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
  var url = $('#id_loginstatus').attr("loginstatus_url");
  $.ajax({
    url:url,
    type:"POST",
    headers:{'X-CSRFToken':csrftoken},
    datatype:'json',
    data:{},
    success:function(data){
      if(data['status']===1){
        submit_post();
        console.log("Form data is submitted");
      }
      else{
        console.log("login required");
        // login logic goes here
      }
    }
  })
}

function submit_post(){
    // console.log("Your Form Is valid, ready to submit");
    const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
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

function check_post_form_valid(){
  if (($.trim($("#id_title").val()).length === 0 ) ||
      ($.trim($("#id_content").val()).length === 0))
      {return false;}
  else
      {return true;}
}

function post_form_add_invalid(){
  $("#id_title").addClass("is-invalid");
  $("#id_content").addClass("is-invalid");
  // console.log("Fill in the required fields");
}

function post_rem_invalid(){
  $("#id_title").removeClass("is-invalid");
  $("#id_content").removeClass("is-invalid");
}
