$(init);

var updateTimer;

function init() {
    $("#messages").scrollTop($("#messages").prop("scrollHeight"));
    $("body").addClass("disableScrolling"); // A scroll bar would appear on the page
    $("#defaultMessage").hide()

    $("#message").keyup(function(event) {
        if (event.keyCode == 13) {
            var text = $("#message").val().trim();
            if (text != "")
                sendMessage(text);
        }
    })

    $("#messageSend").click(function() {
        var text = $("#message").val().trim();
        if (text != "")
            sendMessage(text);
    });

    updateTimer = setInterval(checkForNewMessages, 800);

    displayAllMessages();
}

function displayAllMessages() {
    $.ajax(`/api/chat/${CHAT_ID}/allmessages`, {
        method: 'GET',
        success: function(response) {
            updateMessageList(response);
        }
    });
}

function checkForNewMessages() {
    $.ajax(`/api/chat/${CHAT_ID}/update`, {
        method: 'GET',
        success: function(response) {
            updateMessageList(response);
        },
        error: function() {
            console.log('Something went wrong. Stopping updates');
            updateTimer.stop();
        }
    });
}

function sendMessage(message) {
    $.ajax(`/api/chat/${CHAT_ID}/send`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        },
        data: {
            'message': message
        },
        success: function(response) {
            if (response.success == 1)
                $("#message").val("");
        }
    });
}

function updateMessageList(response) {
    if (!$.isEmptyObject(response)) {
        for (var i = 0; i < response.message_count; i++) {
            var message = response.messages[i];
            var sender = response.senders[message.sender_id]
            var newNode = newNode = $(".message#prototypeMessage").clone().removeAttr("id");

            newNode.children(".messageProfile").attr("src", sender.profile_pic).attr("alt", `${sender.first_name} ${sender.last_name}'s image`);
            newNode.children(".messageBody").html(message.text);
            if (message.sender_id == MY_USER_ID)
                newNode.addClass("to");
            else
                newNode.addClass("from");

            newNode.insertAfter($(".message:last"));
            newNode.show();
        }
        $("#messages").scrollTop($("#messages").prop("scrollHeight"));
    }
}