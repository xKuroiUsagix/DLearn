from course.models import Course, UserCourse


def context_add_courses(context, user):
    my_courses = []
    context_copy = context.copy()
    
    users_course = UserCourse.objects.filter(user=user)
    for user_course in users_course:
        my_courses.append(user_course.course)
    
    context_copy['my_courses'] = my_courses
    context_copy['created_courses'] = Course.objects.filter(owner=user)
    
    return context_copy
