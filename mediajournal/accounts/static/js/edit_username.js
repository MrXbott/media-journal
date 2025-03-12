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
    $('#save_username').on('click', function(){
        $('#message_username').text('');
        console.log('button pressed', $('#username').val());

        new_username = $('#username').val();
        if (new_username){
            $.ajax({
                url: '/accounts/profile/edit_username/',
                type: 'POST',
                dataType: 'json',
                data: {'username': new_username},
                success: function(json){
                    console.log(json);
                    $('#message_username').text(json['message']);
                },
                error: function(xhr, errmsg, err){
                    console.log(err);
                    // console.log(json);
                    $('#message_username').text('Что-то не работает на сервере. Имя не обновлено');
                }
            });
        }
        else {
            $('#message_username').text('Сначала введите свое имя');
        }
        
    });
})