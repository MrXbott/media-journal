
$(document).ready(function () {
  $('.subscription-email-form').on('submit', function (e) {
    e.preventDefault();  

    const form = $(this);
    const actionUrl = form.attr('action');
    const method = form.attr('method');
    const csrfToken = form.find('[name=csrfmiddlewaretoken]').val();
    const emailInput = form.find('input[type=email]');
    const email = emailInput.length ? emailInput.val() : null;
    const $button = form.find('button[type=submit]');
    const originalBtnText = $button.html();

    const formData = {
      csrfmiddlewaretoken: csrfToken,
    };

    // Если гость и не ввёл email — прерываем отправку
    if (emailInput.length && (!email)) {
        showAlert('Пожалуйста, введите корректный email.', 'danger', form);
        return;
    }

    if (email) {
      formData.email = email;
    }

    // блокируем кнопку, показываем загрузку
    $button.prop('disabled', true).html('<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>Подписка...');

    $.ajax({
      type: method,
      url: actionUrl,
      data: formData,
      success: function (response) {
        showAlert('Вы успешно подписались на рассылку!', 'success', form);

        if (emailInput.length) {
          emailInput.val(''); 
        }
      },
      error: function (xhr) {
        let msg = 'Произошла ошибка. Попробуйте ещё раз.';
        if (xhr.responseJSON && xhr.responseJSON.message) {
          msg = xhr.responseJSON.message;
        }
        showAlert(msg, 'danger', form);

      },
      complete: function () {
        // возвращаем кнопку в исходное состояние
        $button.prop('disabled', false).html(originalBtnText);
        }
    });
  });


  function showAlert(message, type, form) {
    const $alert = $(`
      <div class="alert alert-${type} mt-3 mb-0" role="alert">
        ${message}
      </div>
    `);

    form.next('.alert').remove(); // удалить предыдущее сообщение
    form.after($alert);

    setTimeout(() => $alert.fadeOut(500, () => $alert.remove()), 4000);
  }
});
