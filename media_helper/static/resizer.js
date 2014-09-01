// this was taken directly from https://docs.djangoproject.com/en/1.6/ref/contrib/csrf/
// except for the last couple lines.  You should edit the ajax request to fit your needs

$(document).ready(function(){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
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
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
           }
        }
    }); 

    function strip_path(path, position){
        // If position is not defined, set it to 4
        
        //media_root = 
        path.replace(window.location.origin, "")
        position = typeof position !== 'undefined' ? position : 4;
        return path.split('/').slice(position).join("/");
        
    }
    function new_width(element){
        return Math.floor(element.width() * window.screen.width/$(window).width())
    }

    var images = "[";
    var image = ""
    $('img').each(function(){
        image = strip_path($(this)[0].src);
        images += "('" + image + "'," + new_width($(this)) + "), ";
    });

    images += "]";

 
    backgrounds = "["
    background_list = []

    $('div').each(function(){
        if ($(this).css('background-image') != "none"){
            background = strip_path($(this).css('background-image'));
            if background != "undefined"{
                backgrounds += "('" + background.substring(0, background.length-1) + "'," + new_width($(this)) + "), ";
                background_list.push($(this));
            }
        }
    });

    backgrounds += "]"
    //alert(backgrounds + images);
    //backgrounds = find_backgrounds()
    function update_images(data){
        alert(data.length)
        //a = $.parseJSON(data[0]);
        //$.each(data), function(){
            //alert($(this));
        //}
    }
    alert(1);
    $.ajax({
        type: "POST",
        url: '/media-helper/resolution/',
        data: {
            'width' :window.screen.width,
            'height': window.screen.height,
            'images': images,
            'backgrounds': backgrounds
        },
        success: function(data){
            $('img').each(function(){
                //alert(data['images']['/media/bilder/Logo_jumediavision.png']);
                //alert(data['images']["/" + strip_path($(this)[0].src, 3)]);
                $(this).attr('src', data['images']["/" + strip_path($(this)[0].src, 3)]);
            });
            $.each(background_list, function(){
                if $(this) != undefined{
                    url = $(this).css('background-image').split("(")[1].split(")")[0];
                    $(this).css('background-image', 'url("' + data['backgrounds']["/" + strip_path(url, 3)] + '")');
                }

            });
        }
        
    });
});