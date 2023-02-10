function user_auth(){
  username = $("#id_username").val();
  password = $("#id_password").val();
  csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
  authenticate_user(csrftoken,username,password);
}
function authenticate_user(CSRFTOKEN,USERNAME,PASSWORD)
{
  const csrftoken = CSRFTOKEN;
  var url = $('#id_modallogin_url').attr("modallogin_url");
  $.ajax(
    {
      async:true,
      url:url,
      type:"POST",
      headers:{'X-CSRFToken':csrftoken},
      datatype:'json',
      data:{'username':USERNAME,'password':PASSWORD},
      success:function(data){
        if(data['status']===1){
          console.log("Login Success");
          $('input[name="csrfmiddlewaretoken"]').val(data['csrftoken']);
          $("#id_login_modal").modal('hide');
        }
        else{
          console.log("Login Failure");
        }
      }
    }
  )
}
