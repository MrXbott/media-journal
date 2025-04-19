$(document).ready(function() {
    $('#upload-photo-btn').on('click', function(e) {
        e.preventDefault();
        $('#photo-input').click();
    });

    $('#photo-input').on('change', function() {
        const file = this.files[0];
        const errorDiv = $('#photo-errors');
        errorDiv.text('');

        if (!file) return;

        if (!['image/png', 'image/jpeg', 'image/gif'].includes(file.type)) {
            errorDiv.text("Допустимы только файлы PNG и JPG.");
            return;
        }

        if (file.size > 1024 * 1024) {
            errorDiv.text("Файл слишком большой. Максимум 1MB.");
            return;
        }

        const formData = new FormData();
        formData.append('photo', file);

        $('#photo-loader').css('display', 'flex');

        $.ajax({
            url: '/accounts/profile/upload_photo/',
            type: "POST",
            data: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            },
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.status === 'ok') {
                    $('#photo-preview').attr('src', response.photo_url + '?t=' + new Date().getTime());  // cache busting
                } else {
                    errorDiv.text(Object.values(response.errors).flat().join(', '));
                }
                $('#photo-loader').hide();
            },
            error: function(xhr) {
                if (xhr.responseJSON && xhr.responseJSON.errors) {
                    errorDiv.text(Object.values(xhr.responseJSON.errors).flat().join(', '));
                } else {
                    errorDiv.text("Произошла ошибка загрузки.");
                }
                $('#photo-loader').hide();
            }
        });
    });
});

