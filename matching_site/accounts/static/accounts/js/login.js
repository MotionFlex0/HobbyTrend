$(init);

function init() {
    $("#registerButton").click(register);
    $("#loginButton").click(login);

    $("#logRegButton").click(toggleLoginRegister);

    $("#day, #month, #year").on("input", updateFormattedDate);

    //By default, we start at the register page. So change page if the URL is for login
    if (window.location.pathname == "/accounts/login/")
        toggleLoginRegister();
}

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

function register() {
    if (validateRegisterForm()) {
        $("#register").submit();
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
