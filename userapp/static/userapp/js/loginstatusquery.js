//Function to query the login status of user
//SUCCESS_FUNCTION is passed as a parameter, if user is logged in, function is Executed
//CSRFTOKEN and URL is also passed as parameter to enable protability
function loginstatusquery(SUCCESS_FUNCTION,CSRFTOKEN,URL){
  const csrftoken = CSRFTOKEN;
  var url = URL;
  $.ajax({
    async:true,
    url:url,
    type:"POST",
    headers:{'X-CSRFToken':csrftoken},
    datatype:'json',
    data:{},
    success:function(data){
      if(data['status']===1){
        $('input[name="csrfmiddlewaretoken"]').val(data['csrftoken']);
        SUCCESS_FUNCTION(data['csrftoken']);
        console.log("Form data is submitted");
      }
      else{
        console.log("login required");
        if(data.hasOwnProperty('login_modal')){
          $("#id_modal_placeholder").html(data['login_modal']);
          $('input[name="csrfmiddlewaretoken"]').val($("#id_loginstatusquery_csrf").val());
          $("#id_login_modal").modal('show');
        }
      }
    }
  })
}
