from django.utils.translation import gettext_lazy as _


class ErrorMessages:
    PASSWORD_VALIDATION_ERROR = _('Пароль надто слабкий')
    PASSWORD_NOT_MATCH_ERROR = _('Паролі не одинакові')
    BAD_PASSWORD_ERROR = _('Не правильний пароль')
    BAD_PASSWORD_OR_JOINCODE_ERROR = _('Не правильний код приєднання або пароль')
    
    SUPERUSER_ROLE_ERROR = _('Superuser must have role set to 1')
    SUPERUSER_IS_SUPERUSER_ERROR = _('Superuser must have is_superuser set to True')
    
    EMAIL_NOT_GIVEN_ERROR = _('The Email must be given')
    USER_NOT_FOUND_ERROR = _('Не вірний логін чи пароль')
    USER_ALREADY_JOINED_ERROR = _('Ви вже долучилися до цього курсу')
    USER_IS_OWNER_ERROR = _('Ви є власником цього курсу')
