// $(document).ready(function() {
//   $('body').on('submit','#id_post_form',function(event){
//     event.preventDefault();
//     main_func();
//   })});


// $(document).ready(function(){
//   $('#id_post_form').on('submit', function (event) {
//     // console.log($('#id_title')[0])
//     var form_valid = $('#id_post_form')[0].checkValidity();
//     console.log(form_valid);
//     if(form_valid){
//       $('#id_post_form').addClass('was-validated')
//     }
//     event.preventDefault()
//     // event.stopPropagation()
//     if(form_valid) {
//     }
//   })
// })


// function main() {
//   $('#id_post_form').addEventListener('submit', function (event)) {
//     if(form.checkValidity();) {
//       event.preventDefault();
//       event.stopPropagation();
//     }
//   })
// }

function main_func(){
  var form_is_valid = check_post_form_valid();
  if (form_is_valid){
    loginstatuscheck();
    }
  else {console.log("Form Invalid");}
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
