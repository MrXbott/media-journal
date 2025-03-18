

$(document).ready(function(){
    var article_id = $('form#comment #id_article').val();
    var parent_comment_id = '';

    $(document).on('submit', 'form#comment', function(e){
        e.preventDefault();
        var formData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: '/comment/',
            data: formData,
            success: function(json){
                if (json['status'] == 'ok'){
                    $('textarea#id_body').val('');
                    $('#submit-message').text('Your comment will be published after moderation');
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