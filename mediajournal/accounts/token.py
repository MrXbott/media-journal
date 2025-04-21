from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Генератор токенов для подтверждения email пользователя.

    Наследуется от PasswordResetTokenGenerator и переопределяет метод `_make_hash_value`, 
    добавляя статус `is_active` в хеш. Это гарантирует, что токен становится недействительным 
    после активации аккаунта.
    """
    def _make_hash_value(self, user, timestamp: int) -> str:
        """
        Формирует строку для хеширования токена.

        Включает ID пользователя, метку времени и статус активации,
        чтобы токен был уникальным и одноразовым.

        Аргументы:
            user: Объект пользователя.
            timestamp (int): Временная метка, обычно в формате int.

        Возвращает:
            str: Строка, используемая для генерации хеша токена.
        """
        return f'{user.id}{timestamp}{user.is_active}'
    
email_verification_token = EmailVerificationTokenGenerator()

