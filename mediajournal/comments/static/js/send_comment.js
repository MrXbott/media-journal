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

$(document).ready(function(){
    var object_id = $('form#comment-form').attr('data-id');
    var content_type = $('form#comment-form').attr('data-type');
    var parent_comment_id = '';
    console.log('id', object_id, content_type);

    $('form#comment-form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/comment/',
            data: {
                'object_id': object_id,
                'content_type': content_type,
                'text': $('form#comment-form textarea#comment').val(),
                'parent': '',
                },
            success: function(json){
                if (json['status'] == 'ok'){
                    $('textarea#comment').val('');
                    $('#message').text('Ваш комментарий отправлен и будет опубликован после модерации');
                    $('#message').removeClass('hide');
                }
                else {
                    console.log(json['message']);
                }
            },
            error: function(xhr, errmsg, err){
                console.log(xhr.status);
            }
        });
    });

    $(document).on('click', 'div.answer', function(){
        console.log('answer clicked');
        let comment_div = $(this).parent();
        parent_comment_id = $(this).attr('data-id');
        console.log(parent_comment_id);
        $.ajax({
            type: 'GET',
            url: '/comment/',
            data: {'parent_id': $(this).attr('data-id'), 'article_id': $('form#comment #id_article').val()},
            success: function(data){
                if (data != ''){
                    $(comment_div).append(data);
                }
            },
            error: function(xhr, errmsg, err){
                console.log(xhr.status);
            }
        });
    });

    $(document).on('submit', 'form#comment-answer', function(e){
        e.preventDefault();
        var answer_form = this;
        var formData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: '/comment/',
            data: formData,
            success: function(json){
                if (json['status'] == 'ok'){
                    $($(answer_form).parent()).remove();
                    $('#submit-message').text('Your comment will be published after moderation');
                }
            },
            error: function(xhr, errmsg, err){
                console.log(xhr.status);
            }
        });
    });
});