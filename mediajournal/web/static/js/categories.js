$(document).ready(function(){
    $.ajax({
        type: 'GET',
        url: '/categories/',
        success: function(json){
            console.log(json);
            $.each(json, function(name, url){
                $('#categories').append(`<div><a href=${url}>${name}</a></div>`);
            });
        },
        error: function(xhr, errmsg, err){
            console.log(err);
        }
    });
});