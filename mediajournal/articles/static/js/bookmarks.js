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

    $(document).on('click', '.bookmark-icon', function(e){

        console.log('bookmark clicked', user_auth);
        // e.stopPropagation();
        e.preventDefault(); 

        if(!user_auth){
            $('.popup').remove();
            $(this).parent().append(
                $('<div>').attr({'class': 'popup'}).append($('<span>').attr({'class': 'popuptext'}).text('please login').toggleClass('show'))
            );
        }
        else{
            let article_id = $(this).data('id');

            let bookmark_clicked = this;
            $.ajax({
                type: 'POST',
                url: '/bookmark/', 
                data: {
                    'article_id': article_id, 
                }, 
                success: function(data){
                    if (data['bookmark'] == 'added'){
                        $(bookmark_clicked).find('img#unlk').addClass('hide');
                        $(bookmark_clicked).find('img#lk').removeClass('hide');
                    }
                    else if (data['bookmark'] == 'removed') {
                        $(bookmark_clicked).find('img#unlk').removeClass('hide');
                        $(bookmark_clicked).find('img#lk').addClass('hide');
                    }
                },
                error: function(xhr, errmsg, err){
                    console.log(xhr.status);
                }
            });
        }
    });
});

