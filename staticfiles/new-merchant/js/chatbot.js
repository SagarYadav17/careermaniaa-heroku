$(document).ready(function(){
    $(".chatbutton").click(function(){
        $(".chatbutton").removeClass("active");
        let buttonValue = $(this).val();
        if(buttonValue == "custom message"){
            $('.chatbot_buttons').css("z-index","1");
            $('.chat_functionality').addClass('hide');
            $('.custom_message').removeClass('hide');
        }else{
            $('.chatbot_buttons').css("z-index","2");
            $('.chat_functionality').removeClass('hide');
            $('.custom_message').addClass('hide');
        }
        $(this).addClass('active');
    })
    $("#chat_send").click(function(){
        let message = $("#chat_input").val()
        console.log("your message is ",message)
        if(message !=""){
            let constract_message = '<div class="container darker"><img src="" alt="Avatar" class="right" style="width:100%;"><p>'+message+'</p></div>'
            let cur_chat_space = $('.chat_space').html();
            console.log("cur_chat_space ",cur_chat_space);
            let whole_message = cur_chat_space + constract_message;
            setInterval(updateScroll(),1000);
            console.log("whole_message ",whole_message);
            $('.chat_space').html(whole_message);
        }
        $("#chat_input").val("");
    })
    $(".chat_space").on('scroll', function(){
        scrolled=true;
    });
    var scrolled = false;
    function updateScroll(){x
        if(!scrolled){
            var element = $(".chat_space");
            let element_height = element[0].scrollHeight;
            console.log("element.scrollHeight ",element[0].scrollHeight);
            $(".chat_space").scrollTop(element_height);
        }
    }
        
    $("#chat_input").keyup(function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            $("#chat_send").click();
        }
    });
})