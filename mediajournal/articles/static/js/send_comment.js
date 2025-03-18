
$(document).ready(function(){
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
});