$(document).ready(function(){
    $(".dropdown").select2();    
    var url = window.location.href;
    let value = url.split("value=")[1]
    if(value == "class"){
        let self = $("#class_btn");
        classButton(self)
    }else if(value == "college"){
        let self = $("#college_btn");
        collegeButton(self);
    }else if(value == "job") {
        let self = $("#job_btn");
        jobButton(self);
    }

    $("#college_btn").click(function(){
        let self = $(this)
        collegeButton(self);
    })

    $("#class_btn").click(function(){
        let self = $(this);
        classButton(self)
    })

    $("#job_btn").click(function(){
        let self = $(this)
        jobButton(self);
    })

    function collegeButton(self){
        self.closest("div").find(".btn").each(function(){
            $(this).removeClass("active");
        })
        self.addClass("active")
        $("#main_form").find("#form_define").val("colleges");
        $("#main_form").find(".left-form .email_id #email_title").html("College Email id *")
        $("#main_form").find(".right-form .head_name #head_name_title").html("Chancellor/Chairman")
        $("#main_form").find(".right-form .address #address_title").html("Collage Address ")
        $("#main_form").find(".left-form .merchent_name #merchent_name_title").html("Collage Name")
        $("#main_form").find(".left-form .selector-group .selector").each(function(){
            $(this).addClass("hide");
        })
        $("#main_form").find(".left-form .selector-group .college_info").removeClass("hide")
    }

    function classButton(self){
        self.closest("div").find(".btn").each(function(){
            $(this).removeClass("active");
        })
        self.addClass("active")
        $("#main_form").find("#form_define").val("classes");
        $("#main_form").find(".left-form .email_id #email_title").html("Class Email id *")
        $("#main_form").find(".right-form .head_name #head_name_title").html("Directors Name")
        $("#main_form").find(".right-form .address #address_title").html("Center Address ")
        $("#main_form").find(".left-form .merchent_name #merchent_name_title").html("Class Name *")
        $("#main_form").find(".left-form .selector-group .selector").each(function(){
            $(this).addClass("hide");
        })
        $("#main_form").find(".left-form .selector-group .class_info").removeClass("hide")
    }

    function jobButton(self){
        self.closest("div").find(".btn").each(function(){
            $(this).removeClass("active");
        })
        self.addClass("active")
        $("#main_form").find("#form_define").val("jobs");
        $("#main_form").find(".left-form .email_id #email_title").html("Employer Email id *")
        $("#main_form").find(".right-form .head_name #head_name_title").html("Directors Name")
        $("#main_form").find(".right-form .address #address_title").html("Company Address ")
        $("#main_form").find(".left-form .merchent_name #merchent_name_title").html("Company Name *")
        $("#main_form").find(".left-form .selector-group .selector").each(function(){
            $(this).addClass("hide");
        })
        $("#main_form").find(".left-form .selector-group .job_info").removeClass("hide")
    }
})