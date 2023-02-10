$("#id_post_form").validate({
  degug:true,
  submitHandler: function(form) {
    var url = $('#id_loginstatus').attr("loginstatus_url");
    console.log("Submit Handler")
    console.log($(form).csrftoken);
    $(form).ajaxSubmit({url: url, type: 'POST',encode: true});
  }
});

// Not Implemented but kept for future use and reference
//
// for form validation use the following script
// <script src="http://ajax.aspnetcdn.com/ajax/jquery.validate/1.11.1/jquery.validate.min.js"></script>
//
// for ajaxSubmit use the following script
// <script src="https://malsup.github.io/jquery.form.js"></script>
