var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function() {
    $messages.mCustomScrollbar();

    setTimeout(function() {
        if ($('.message-input').val() != '') {
        return false;
    }
    $('<div class="message loading new"><figure class="avatar"><img src="img/bat.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    updateScrollbar();

    setTimeout(function() {
        $('.message.loading').remove();
        console.log(JSON.stringify(reply))
        $('<div class="message new"><figure class="avatar"><img src="img/bat.png" /></figure>' + "Hello there!" + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        updateScrollbar();
        i++;
    }, 1000 + (Math.random() * 20) * 100);
    }, 100);
});










function updateScrollbar() {
    $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
        scrollInertia: 10,
        timeout: 0
    });
}

function setDate() {
    d = new Date()
    if (m != d.getMinutes()) {
        m = d.getMinutes();
        $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
    }
}

var reply = "";

function insertMessage() {
    msg = $('.message-input').val();

    // Invoking chatbot API

    const url = 'https://xpytv865vl.execute-api.us-east-1.amazonaws.com/v1/chatbot';
    const data = JSON.stringify({
  "messages": [
    {
      "type": "string",
      "unstructured": {
        "id": "string",
        "text": msg,
        "timestamp": "string"
      }
    }
    ]
    });

    //console.log(data);
    




    if ($.trim(msg) == '') {
        return false;
    }
    $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    $('.message-input').val(null);
    updateScrollbar();
    // setTimeout(function() {
    //     fakeMessage();
    // }, 1000 + (Math.random() * 20) * 100);


    var apigClient = apigClientFactory.newClient();


    var body = JSON.stringify({
  "messages": [
    {
      "type": "string",
      "unstructured": {
        "id": "string",
        "text": msg,
        "timestamp": "string"
      }
    }
    ]
    });

    apigClient.chatbotPost({}, body)
    .then(function(result){
        //This is where you would put a success callback
        //console.log(result["data"]["messages"][0]["unstructured"]["text"]);
        console.log(result)
        var reply = result["data"]["messages"][0]["unstructured"]["text"]
        fakeMessage(reply)
    }).catch( function(result){
        //This is where you would put an error callback
        console.log(result);
    });


    // $.post(url, data, function(reply, status) {
    //     console.log(JSON.stringify(reply) + "and status is" + status) 
    //     fakeMessage(reply)
    // });
}

$('.message-submit').click(function() {
    insertMessage();
});

$(window).on('keydown', function(e) {
    if (e.which == 13) {
        insertMessage();
        return false;
    }
})

// var Fake = [
//     'Hi there, I\'m BATMAN and you?',
//     'Do you wanna know My Secret Identity?',
//     'Nice to meet you',
//     'How are you?',
//     'Not too bad, thanks',
//     'What do you do?',
//     'That\'s awesome',
//     'Codepen is a nice place to stay',
//     'I think you\'re a nice person',
//     'Why do you think that?',
//     'Can you explain?',
//     'Anyway I\'ve gotta go now',
//     'It was a pleasure chat with you',
//     'Bye',
//     ':)'
// ]

function fakeMessage(reply) {
    if ($('.message-input').val() != '') {
        return false;
    }
    $('<div class="message loading new"><figure class="avatar"><img src="img/bat.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    updateScrollbar();

    setTimeout(function() {
        $('.message.loading').remove();
        //console.log(reply["data"]["messages"][0]["unstructured"]["text"]);
        $('<div class="message new"><figure class="avatar"><img src="img/bat.png" /></figure>' + reply + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        updateScrollbar();
        i++;
    }, 1000 + (Math.random() * 20) * 100);

}
