
$(document).ready(function(){
    $(document).on('submit', '#comment', function(e){
        e.preventDefault();

        console.log('submit comment pressed');
        console.log($('#id_text').val(), $('#article_id').val());
        $.ajax({
            type: 'POST',
            url: '/comment/',
            data: {
                text: $('#id_text').val(),
                article_id: $('#article_id').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success: function(json){
                console.log(json)
                if (json['status'] == 'ok'){
                    console.log('comment saved');  
                    let comment_text = '<b>'+ json['created'] + ' ' + json['username'] +'</b> ' + json['comment'];
                    $('div#comments').append($('<div>').attr({'class': 'comment'}).html(comment_text));
                    $('textarea#id_text').val('');
                }
                
            },
            error: function(xhr, errmsg, err){
                console.log(xhr.status);
            }
        });
    });
});