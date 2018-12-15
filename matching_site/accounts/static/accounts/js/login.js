'FileReader' in window
$(init);

function init() {
    $("#registerButton").click(register);
    $("#loginButton").click(login);
    $("#submitImage").click(submitImage);

    $("#logRegButton").click(toggleLoginRegister);


    $("#day, #month, #year").on("input", updateFormattedDate);

    $('#file').on('change', function(){
        readURL(this);
    });

    //By default, we start at the register page. So change page if the URL is for login
    if (window.location.pathname == "/accounts/login/")
        toggleLoginRegister();
}

var droppedFile = false;

  $('#uploadInput').on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
  })
  .on('dragover dragenter', function() {
    $('#uploadInput').addClass('is-dragover');
  })
  .on('dragleave dragend drop', function() {
    $('#uploadInput').removeClass('is-dragover');
  })
  .on('drop', function(e) {
    droppedFile = e.originalEvent.dataTransfer.files[0];
    if (droppedFile.type.indexOf("image") == 0) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#uploadInput').css({'background': 'url('+ e.target.result +')', 'background-size': 'cover'})
            $('#fileLabel').css('display', 'none');
        }
        reader.readAsDataURL(droppedFile);
    }
  });


function toggleLoginRegister() {
    $("#register").toggle();
    $("#login").toggle();

    var registerPage = $("#register").is(":visible");

    if (registerPage) {
        $("#logRegButton").html("login");
        history.replaceState(null, "Register", "/accounts/register/");
    }
    else {
        $("#logRegButton").html("register");
        history.replaceState(null, "Login", "/accounts/login/");
    }
}
function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      console.log("can read");
      reader.onload = function(e) {
        $('#uploadInput').css({'background': 'url('+ e.target.result +')', 'background-size': 'cover'})
        $('#fileLabel').css('display', 'none');
      }
      reader.readAsDataURL(input.files[0]);
    }
}

function register() {
    if (validateRegisterForm()) {
        $("#register").submit();
    }
}

function submitImage() {
    if (validateImageForm()) {
        if ($("#file").val() == '' && droppedFile != ''){
            console.log("send dragged image");
            var ajaxData = new FormData( "file", droppedFile )
            $.ajax({
                url: "/accounts/imageUpload/",
                type: "POST",
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
                data: ajaxData,
                dataType: 'json',
                cache: false,
                contentType: false,
                processData: false,
                complete: function() {
                  console.log("complete");
                },
                success: function(data) {
                    console.log(data);
                },
                error: function(error) {
                    console.log(error);
                    // Log the error, show an alert, whatever works for you
                }
              })
        } else if ($("#file").val() != '' && droppedFile == ''){
            $("#imageUpload").submit();
        }
    }
}

function login() {
    if(validateLoginForm()) {
        $("#login").submit();
    }
}

function validateRegisterForm() {
    var success = true;
    $("#register > input, #register > * > input").not("[name=csrfmiddlewaretoken]").each(function(){
        if ($(this).val() == ""){
            $(this).css("border", "1px solid red");
            success = false;
        }
        else
            $(this).css("border", "0px");
    });
    
    return success;
}

function validateImageForm() {
    var success = true;

    if($("#file").val() == '' && droppedFile == ''){
        success =  false;
    }
    console.log(success);
    return success;
}

function validateLoginForm() {
    var success = true;
    $("#login > input").each(function(){
        if ($(this).val() == ""){
            $(this).css("border", "1px solid red");
            success = false;
        }
        else
            $(this).css("border", "0px");
    });
    
    return success;
}

//Keeps an update version of the date, required for form validation on the server
function updateFormattedDate() {
    var datePart = $(this).attr("id");
    if (datePart == 'day'){
        var currentVal = $("#dob").val();
        $("#dob").val(currentVal.replace(/(\d*-\d*-)\d*/, `$1${$(this).val()}`))
    }
    else if (datePart == 'month'){
        var currentVal = $("#dob").val();
        $("#dob").val(currentVal.replace(/(\d*-)\d*(.*)/, `$1${$(this).val()}$2`))
    }
    else if (datePart == 'year'){
        var currentVal = $("#dob").val();
        $("#dob").val(currentVal.replace(/\d*(.*)/, `${$(this).val()}$1`))
    }
}
