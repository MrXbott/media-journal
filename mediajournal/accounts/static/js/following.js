var csrftoken = Cookies.get('csrftoken'); 
function csrfSafeMethod(method) {
    // Для этих методов токен не будет подставляться в заголовок.
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)); 
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) { 
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        } 
    }
});

$(document).ready(function(){

    $('.follow-btn').on('click', function(e){
        e.preventDefault();
        var follow_btn = this;
        var followers_counter_element = $('#followers-counter');
        var counter = parseInt($('#followers-counter').text());
        var user_id = $(this).data('id');
        var action = $(this).data('action');
        $.ajax({
            type: 'POST',
            url: '/accounts/follow/', 
            data: {
                'user_id': user_id, 
                'action': action,
            }, 
            success: function(data){
                if (data['status'] == 'ok'){
                    if (action == 'follow'){
                        $(follow_btn).text('Отписаться');
                        $(follow_btn).attr({'data-action': 'unfollow'});
                        $(followers_counter_element).text(counter + 1);
                    }
                    else if (action == 'unfollow'){
                        $(follow_btn).text('Подписаться');
                        $(follow_btn).attr({'data-action': 'follow'});
                        $(followers_counter_element).text(counter - 1);
                    }
                    
                }
                else if (data['status'] == 'error') {
                    console.log(data['message']);
                }
            },
            error: function(xhr, errmsg, err){
                console.log(xhr.status);
            }
        });
        
    });
});