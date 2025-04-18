$(document).ready(function () {
  $('#subscribe-btn').on('click', function (e) {
    e.preventDefault();

    const $btn = $(this);
    const $state = $('#is-subscribed');
    const isSubscribed = $state.val() === '1';
    const originalText = $btn.html();
    const actionUrl = isSubscribed ? '/unsubscribe/' : '/subscribe/';

    $btn.prop('disabled', true).html(
      '<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>Обработка...'
    );

    $.ajax({
      url: actionUrl,
      type: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken(),
      },
      success: function (response) {
        if (isSubscribed) {
          // Был подписан — теперь отписан
          $btn
            .removeClass('btn-danger')
            .addClass('btn-primary')
            .html('Подписаться на рассылку');
          $state.val('0');
          showAlert('Вы успешно отписались от рассылки.', 'success');
        } else {
          // Был не подписан — теперь подписан
          $btn
            .removeClass('btn-primary')
            .addClass('btn-danger')
            .html('Отписаться от рассылки');
          $state.val('1');
          showAlert('Вы успешно подписались на рассылку.', 'success');
        }

        $btn.prop('disabled', false);
      },
      error: function (xhr) {
        let msg = 'Произошла ошибка. Попробуйте позже.';
        if (xhr.responseJSON && xhr.responseJSON.message) {
          msg = xhr.responseJSON.message;
        }
        showAlert(msg, 'danger');
        $btn.prop('disabled', false).html(originalText);
      }
    });
  });

  function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
           Cookies.get('csrftoken'); 
  }

  function showAlert(message, type) {
    const $alert = $(`
      <div class="alert alert-${type} position-fixed top-0 start-50 translate-middle-x mt-3 w-auto z-3" style="z-index: 1055;" role="alert">
        ${message}
      </div>
    `);
    $('body').append($alert);
    setTimeout(() => $alert.fadeOut(500, () => $alert.remove()), 4000);
  }
});

