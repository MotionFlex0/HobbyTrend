$(init);

//This function runs when the page loads. It adds all the event listener for home.html
function init() {
    $("#myProfile").click(function() {
        showProfile($(this).data('userId'));
    });

    $("#exitImage").click(function() {
        $("#profileOverlay").hide();
        $("body").removeClass("disableScrolling");
        history.replaceState(null, "Profile", `/`);
    })

    $("#addHobby").click(addHobby);
    $("#removeHobby").click(removeHobby);

    $('input[type=checkbox][name=gender]').change(refreshUserList);

    $('#minAge, #maxAge').on("input", function() {
        if (validateAge(this))
            refreshUserList();
    });

    var openProfile = window.location.pathname.match(/^\/profile\/([\d]+)$/);
    if (openProfile)
        showProfile(parseInt(openProfile[1]))

    refreshUserList();
}

function allowDrop(ev) {
    ev.preventDefault();
}
  
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}
  
function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
}

//This function refreshs the user list on the home page.
function refreshUserList() {

    var selectedGenders = [];
    var gender = "";
    
    $("input[name=gender]:checked").each(function() {
        selectedGenders.push($(this).val());
    });

    if (selectedGenders.length > 1)
        gender = "Both";
    else if(selectedGenders.length == 0)
        gender = "None";
    else
        gender = selectedGenders[0];

    $.ajax('/api/getcommonusers', {
        method: 'GET',
        data: {
            gender: gender,
            minAge: $("#minAge").val() || 0,
            maxAge: $("#maxAge").val() || 99,
        },
        success: function(userListData) {
            if (userListData.length > 0) {
                $("#commonUserContainer > .commonUser").not("#defaultCommonUser").remove();
                
                $("#defaultCommonUser").show();

                for (var i = 0; i < userListData.length; i++) {
                    var newNode; 
                    var userData = userListData[i];

                    if (i > 0)
                        newNode = $(".commonUser:last").clone().removeAttr("id");
                    else
                        newNode = $(".commonUser");
                    
                    newNode.data("userId", userData.id);
                    newNode.find("#hobbyList").empty();
                    newNode.find("#userHeading").html(`${userData.name_formatted}<br><span class="light">${userData.common_hobbies} hobbies in common</span>`);
                    newNode.find("#profilePic").attr("src", userData.profile_pic).attr("alt", `${userData.first_name} ${userData.last_name}'s image`);                 
                    newNode.find("#viewProfile").data("userId", userData.id).click(function() {
                        showProfile($(this).data("userId"));
                    });
                    $.each(userData.hobbies, function(index, data) {
                        newNode.find("#hobbyList").append(`<li class="hobbyItem">${data}</li>`)
                    });

                    if (i != 0)
                        newNode.insertAfter($(".commonUser:last")); 
                }
            }
            else {
                $("#commonUserContainer > .commonUser").not("#defaultCommonUser").remove();
                $("#defaultCommonUser").hide();
            }

        }
    });
}

//This fuanctoin does a AJAX require for a individual user's information. This information is then shown on the profile page
function showProfile(userId) {
    $.ajax(`/api/user/${userId}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(userData) {
            if (!('error' in userData)) {
                $("#profileViewHobbies").empty();
                $("#profileViewName").html(`${userData.name_formatted}`);
                $("#profileViewEmail").html(`<b>Email:</b> ${userData.email}`);
                $("#profileViewGender").html(`<b>Gender:</b> ${userData.gender}`);
                $("#profileViewBirthday").html(`<b>Birthday:</b> ${userData.dob}`);
                $("#profileImage").attr("src", userData.profile_pic).attr("alt", `${userData.first_name} ${userData.last_name}'s image`);                 
                $.each(userData.hobbies, function(index, value) {
                    if (userData.hobbies.length-1 == index)
                        $("#profileViewHobbies").append(value);
                    else
                        $("#profileViewHobbies").append(`${value}, `);
                });
                if (userId == "me") {
                    $("#messageLogout").html('<button id="logout">Logout</button>');
                    $("#logout").click(function(){
                        window.location = "/accounts/logout/";
                    });

                } else {
                    $("#messageLogout").html(
                        $('<button id="message">Message</button>').click(function() {
                            window.open(`/chat/startchat/${userId}`);
                        })
                    );
                }
                $("#profileOverlay").show();
                $("body").addClass("disableScrolling");
                history.replaceState(null, "Profile", `/profile/${userId}`);
                console.log("state changed");
            }
        }
    });   
}

//This function sends a AJAX request, in order to add a new hobby to the logged in user's profile
function addHobby() {
    $.ajax('/api/user/me/hobbies', {
        method: 'POST',
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        },
        data: {
            hobby: $("#hobbyList").val()
        },
        success: function(result) {
            refreshUserList();
        }
    });
}

//This function allows the user to remove a hobby.
function removeHobby() {
    $.ajax('/api/user/me/hobbies', {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        },
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({
            hobby: $("#hobbyList").val()
        }),
        success: function(result) {
            refreshUserList();
        }
    });
}

//This function validates the age entered, to make sure it is a number.
function validateAge(element) {
    var newValue = $(element).val();
    if (newValue == "" || $.isNumeric(newValue) && $(element).val().length <= 2) {
        $(element).data('last-val', newValue);
        return true;
    }

    $(element).val($(element).data('last-val'));
    return false;
}