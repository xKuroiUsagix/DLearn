from django.utils.translation import gettext_lazy as _


class ErrorMessages:
    
    PASSWORD_VALIDATION_ERROR = _('Passwrod should contains at least 1 character, at least 1 number')
    PASSWORD_NOT_MATCH_ERROR = _('Password and Confirm Password don\'t match')
    BAD_PASSWORD_ERROR = _('Bad password')
    BAD_PASSWORD_OR_JOINCODE_ERROR = _('Bad course Join Code or Password')
    
    SUPERUSER_ROLE_ERROR = _('Superuser must have role set to 1')
    SUPERUSER_IS_SUPERUSER_ERROR = _('Superuser must have is_superuser set to True')
    
    EMAIL_NOT_GIVEN_ERROR = _('The Email must be given')
    USER_NOT_FOUND_ERROR = _('No such user with this email and password')
    USER_ALREADY_JOINED_ERROR = _('You have already joined this course.')
    USER_IS_OWNER_ERROR = _('You are the owner of this course')
