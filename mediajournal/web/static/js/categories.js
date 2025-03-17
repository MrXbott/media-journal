$(document).ready(function(){
    $.ajax({
        type: 'GET',
        url: '/categories/',
        success: function(json){
            $.each(json, function(i, cat){
                $('#categories').append($('<div>').attr({'class': 'category'}).html(`<a href=${cat['url']}><img src="${cat['image']}">${cat['name']}</a>`));
            });
            $('#categories').append($('<div>').html('<a href="/categories/">Смотреть все -></a>'));
        },
        error: function(xhr, errmsg, err){
            console.log(err);
        }
    });
});