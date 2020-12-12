$(document).ready(function(){

    var navbar = document.getElementById("total_navbar");
    var sticky = navbar.offsetTop;
    console.log("sticky = ",sticky);
    window.onscroll = function() {stickyFunction()};
    run();
    hmburgerFunction();
    $(window).resize(function() {
        hmburgerFunction();
    });

    $("#hamburgericon").click(function(){
        myFunction();
    })

    $("#hamburgerMenu .scroll").click(function(){
        myFunction();
    })

    // var count = 1;
    window.setInterval(function(){
        bcvTextChange();
    },2000);

    var scrollLink = $('.scroll');
    // Smooth scrolling
    scrollLink.click(function(e) {
      e.preventDefault();
      $('body,html').animate({
        scrollTop: $(this.hash).offset().top
      }, 1000 );
    });

    $("#ClassesButton").click(function(){
        var origin = window.location.origin;
        window.location.href = origin+'/html/signup.html?value=class';
    })
    $("#CollegesButton").click(function(){
        var origin = window.location.origin;
        window.location.href = origin+'/html/signup.html?value=college';
    })
    $("#JobsButton").click(function(){
        var origin= window.location.origin;
        window.location.href = origin+'/html/signup.html?value=job';
    })

    // $("#background_image").load("./html/background.html");

    // function buttonChange(){
    //     let cur_index = 0;
    //     $("#button_group").find(".showhidebutton").each(function(index){
    //             $(this).fadeOut();
    //             $(this).addClass("hide");
    //         if(index == count){
    //             cur_index = index+1;
    //             $(this).removeClass("hide");
    //             $(this).fadeIn();
    //         }
    //         (index == 2)?((count >= 2)?(count=0):(count= cur_index)):"";
    //     })
    // }


    //////////////////////////////////////////////////////////////////////////////////

    // Add something to given element placeholder
    function addToPlaceholder(toAdd, el) {
        el.attr('placeholder', el.attr('placeholder') + toAdd);
        // Delay between symbols "typing" 
        return new Promise(resolve => setTimeout(resolve, 100));
    }
    // Cleare placeholder attribute in given element
    function clearPlaceholder(el) {
        el.attr("placeholder", "");
    }
    // Print one phrase
    function printPhrase(phrase, el) {
        return new Promise(resolve => {
            // Clear placeholder before typing next phrase
            clearPlaceholder(el);
            let letters = phrase.split('');
            // For each letter in phrase
            letters.reduce(
                (promise, letter, index) => promise.then(_ => {
                    // Resolve promise when all letters are typed
                    if (index === letters.length - 1) {
                        // Delay before start next phrase "typing"
                        setTimeout(resolve, 2000);
                    }
                    return addToPlaceholder(letter, el);
                }),
                Promise.resolve()
            );
        });
    } 
    // Print given phrases to element
    function printPhrases(phrases, el) {
        // For each phrase
        // wait for phrase to be typed
        // before start typing next
        phrases.reduce(
            (promise, phrase,index) => promise.then(_ =>{
                if(index === phrases.length-1){
                    clearPlaceholder(el);
                    setTimeout(run,2000);
                }
                return printPhrase(phrase, el);   
            }), 
            Promise.resolve()
        );
    }
    // Start typing
    function run() {
        console.log("Its hitting");
        let phrases = [
            "Try Login",
            "Try signup",
            "Try Join"
        ];
        printPhrases(phrases, $('#autosuggestfor'));
    }

    $("body").click(function(){
        $("#autosuggestfor").removeClass("open")
        $(".bcv_upperpart .suggestionList").html("");
    })

    $(".bcv_upperpart #autosuggestfor").keyup(function(e){
        let cur_search_value = $("#autosuggestfor").val();
        let search_result = "";
        $(".bcv_upperpart .suggestionList").html(search_result);
        $("#autosuggestfor").removeClass("open")
        if(cur_search_value.length >=3){
            let final_search_value = cur_search_value.toLowerCase();
            final_search_value.includes("log") ? search_result += "<li><a href='./html/login.html'>Login in Careermania</a></li>" : "";
            final_search_value.includes("sig") ? search_result += "<li><a href='./html/signup.html'>Signup in careermania</a></li>" : "";
            final_search_value.includes("joi") ? search_result += "<li><a href='./html/signup.html'>Join in careermania</a></li>" : "";
        }
        if(search_result !=""){
            $("#autosuggestfor").addClass("open")
            $(".bcv_upperpart .suggestionList").html(search_result);
        }
        // console.log(cur_value_exp);
        // console.log(cur_value_exp.test("login"));
    })



    //////////////////////////////////////////////////////////////////////////////////

    let index = 0;
    function bcvTextChange(){
        let buttonTextArray = ["Buisness","Career","Value"];
        $("#showhideTextportion").find(".showhidebutton").html(buttonTextArray[index]);
        index == 2 ? index = 0 : index ++;
    }

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
    function updateScroll(){
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

    function stickyFunction() {
        if (window.pageYOffset >= (sticky+100)) {
            navbar.classList.add("sticky")
        } else {
            navbar.classList.remove("sticky");
        }
    }
    function hmburgerFunction(){
        if(screen.width < 768){
            $("#menu_content").addClass("hide");
            $("#hamburgericon").removeClass("hide");
            // $("#hamburgerMenu").remobveClass("hide");
        }else{
            $("#menu_content").removeClass("hide");
            $("#hamburgericon").addClass("hide");
            $("#hamburgerMenu").css("display","none");
        }
    }

    function myFunction() {
        var x = document.getElementById("hamburgerMenu");
        if (x.style.display === "block") {
          x.style.display = "none";
        } else {
          x.style.display = "block";
        }
      }
})

