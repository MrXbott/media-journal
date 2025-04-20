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
    const user_auth = JSON.parse(document.getElementById('user_auth').textContent);

    $(document).click(function(){
        $('.popup').remove();
    });

    $(document).on('click', 'i[class*="bi-bookmark"]', function(e){

        console.log('bookmark clicked, user auth:', user_auth);
        e.preventDefault(); 

        if(!user_auth){
            $('.popup').remove();
            console.log($(this).parent());
            // var newdiv = $( "<div class='popup'>Please login</div>" );
            $(this).parent().append(
                $('<div>').attr({'class': 'popup'}).append($('<span>').attr({'class': 'popuptext'}).text('please login').toggleClass('show'))
            );
        }
        else{
            let object_id = $(this).data('id');
            let content_type = $(this).data('type');
            console.log('object id, type: ', object_id, content_type);
            let bookmark_clicked = this;
            let count_element = $($(bookmark_clicked).parent()).find('#bookmarks-count');
            let count = parseInt($(count_element).text());
            $.ajax({
                type: 'POST',
                url: '/bookmark/', 
                data: {
                    'object_id': object_id, 
                    'content_type': content_type,
                }, 
                success: function(data){
                    if (data['bookmark'] == 'added'){
                        $(bookmark_clicked).removeClass('bi-bookmark');
                        $(bookmark_clicked).addClass('bi-bookmark-fill');
                        $(count_element).text(count + 1);
                    }
                    else if (data['bookmark'] == 'removed') {
                        $(bookmark_clicked).removeClass('bi-bookmark-fill');
                        $(bookmark_clicked).addClass('bi-bookmark');
                        $(count_element).text(count - 1);
                    }
                },
                error: function(xhr, errmsg, err){
                    console.log(xhr.status);
                }
            });
        }
    });
});

