from .constants import ID_REQUIRED_MESSAGE, ID_NOT_A_NUMBER


def get_course_id_error_message_if_any(course_id):
    if not course_id:
        return ID_REQUIRED_MESSAGE

    try:
        course_id = int(course_id)
    except ValueError:
        return ID_NOT_A_NUMBER
