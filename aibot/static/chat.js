ended = false;
var chat_img_id = 0;
var chat_img_class = 0;
$('#chat-form').on('submit', function(event){
    event.preventDefault();
    var img=["nitesh.jpg","img2.png","img3.png","img4.jpg"]
    var quuery = $('#chat-msg').val();
    $.ajax({
        url : '/post/',
        type : 'POST',
        data : { msgbox : $('#chat-msg').val() },
        beforeSend:function(){
            $('#chat-msg').val('');
            try{
                $('#processing_query').remove();
            }catch(e){}
            $('#msg-list').append('<li style="margin-bottom:5px;" id="processing_query"><span class="text-left response list-group-item animated fadeInUp response-noimg"><div class="chatloader"></div></span></li>');
            chatlist.scrollTop = chatlist.scrollHeight;
        },
        success : function(json){
            if(json.response.toString().toLowerCase() == "what can i call you?")
                $('#chat-msg').val("My name is ");
            $('#chat-msg').focus();
            $('#processing_query').remove();
            try{
                $("#search-book-con").parent().html("...");
            }
            catch(e){}
            if(ended){
                ended = false;
                $("#msg-list li").remove();
                $('#msg-list').append('<li class="text-center draft list-group-item animated fadeInUp">New Session Started</li>');
            }
            if(json.query !="")
                $('#msg-list').append('<li class="text-right list-group-item animated fadeInUp"><div class="query">' + json.query + '</div></li>');
            setTimeout(function(){
                for (var i = 0; i < json.response.length; i++) {
                    resp = json.response[i]
                    if(resp =="")
                        resp = "<span style='color:red;margin-right:30px'><i>No Response from Server!<i><span>";
                    if(i == json.response.length-1)
                        $('#msg-list').append('<li style="margin-bottom:5px;"><img class="chat-img_  animated fadeInLeft" src="/static/'+img[chat_img_id]+'"><span class="text-left response list-group-item animated fadeInUp">' + resp + '</span></li>');
                    else
                        $('#msg-list').append('<li style="margin-bottom:5px;"><span class="text-left response response-noimg list-group-item animated fadeInUp">' + resp + '</span></li>');
                    chatlist.scrollTop = chatlist.scrollHeight;
                }
            },200);
            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
        },
        error: function(){
            $('#processing_query').remove();
            try{
                $("#search-book-con").parent().html("...");
            }
            catch(e){}
            $('#msg-list').append('<li class="text-right list-group-item animated fadeInUp"><div class="query">' + quuery + '</div></li>');
            resp = "<span style='color:red;'><i>Error occured while connecting to Server!<i><span>"
            $('#msg-list').append('<li class="text-left response-noimg response list-group-item animated fadeInUp">' + resp + '</li>');
        }
    });
    chat_img_id++;
    if (chat_img_id>3)
        chat_img_id = 0;
    chatlist.scrollTop = chatlist.scrollHeight;
});
function getMessages() {
    $.ajax({
        url : '/post/',
        type : 'POST',
        data : { getMessages : true },
        beforeSend: function(){
            $('body').append("<div id='loader' style='position:fixed;z-index:99999;top:0;left:0;width:100%;height:100%;background:white;'><div class='loader'></div><div class='loaderText'>Connecting AIbot...</div></div>")
        },
        success : function(json){
            $('#loader').fadeOut();
            if (json==""){
                alert("Retring...")
                setTimeout(getMessages,500);
            }
            else{
                if(json.query !="")
                    $('#msg-list').append('<li class="text-right list-group-item animated fadeInUp"><div class="query">' + json.query + '</div></li>');
                if(json.response !="")
                    setTimeout(function(){
                        $('#msg-list').append('<li style="margin-bottom:5px;"><img class="chat-img_ animated fadeInLeft" src="/static/nitesh.jpg"><span class="text-left response list-group-item animated fadeInUp">' + json.response + '</span></li>');
                        chatlist.scrollTop = chatlist.scrollHeight;
                    },200);
                var chatlist = document.getElementById('msg-list-div');
                chatlist.scrollTop = chatlist.scrollHeight;
            }
        }
    });
}



var scrolling = false;
$(function(){
    $('#msg-list-div').on('scroll', function(){
        scrolling = true;
    });
    // refreshTimer = setInterval(getMessages, 5000);
});
function panle_timer() {
    var d = new Date();
    var days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    hours = d.getHours();
    var ap ="AM";
    if (hours>12){
        hours-=12;
        ap="PM";
    }
    if(hours==12)
        ap="PM";
    if(hours < 10)
        hours="0"+hours
    var seconds = d.getSeconds();
    if(seconds<10)
        seconds="0"+seconds;
    var minutes = d.getMinutes();
    if(minutes<10)
        minutes = "0"+minutes
    $("#panel-time").html(hours+":"+minutes+":"+seconds+" "+ap);
    $("#panel-date").html(months[d.getMonth()]+" "+d.getDate()+", "+d.getFullYear()+" | "+days[d.getDay()]);
}
setInterval(panle_timer,500);
function panel_names(prev,id) {
    img=["nitesh.jpg","img2.png","img3.png","img4.jpg"]
    var timeout = 2000;
    if (id == 1)
        timeout += 2000;
    var next = id+1;
    if(next>4)
        next=1;
    $('#panel-name-'+prev).removeClass().addClass("animated fadeOut");
    $('.chat-img').removeClass().addClass("animated fadeOut chat-img");
    setTimeout(function () {
        $('.chat-img').attr("src","/static/"+img[id-1])
        $('#panel-name-'+id).removeClass().addClass("animated fadeIn");
        $('.chat-img').removeClass().addClass("animated fadeIn chat-img");
        $('#panel-name-'+prev).hide();
        $('#panel-name-'+id).show();
        setTimeout(function() {panel_names(id,next)}, timeout);
    },700);
}
panel_names(1,1);
$(document).ready(function() {
    $('#chat-msg').focus();
    getMessages();
     $('#send').attr('disabled','disabled');
     $('#chat-msg').keyup(function() {
        if($(this).val() != '') {
           $('#send').removeAttr('disabled');
        }
        else {
        $('#send').attr('disabled','disabled');
        }
     });
 });
if(getCookie("sessionID") == null)
    setCookie("sessionID",Math.floor(Math.random() * 99999999999)+"AIbot")
function setCookie(name,value){
    document.cookie = name+"="+value+";";
}
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});