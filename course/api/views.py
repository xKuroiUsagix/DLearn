from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from django.shortcuts import get_object_or_404

from .serializers import CourseSerializer, CourseUpdateSerializer
from .helpers import get_course_id_error_message_if_any

from ..models import Course


class CourseAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseSerializer

    def get(self, request):
        course_id = request.data.get('id')

        if course_id:
            course = get_object_or_404(Course, id=int(course_id))
            serializer = self.serializer_class(instance=course)
            return Response(serializer.data, status=HTTP_200_OK)

        return Response('id is required', status=HTTP_400_BAD_REQUEST)

    def post(self, request):
        confirm_password = request.data.pop('confirm_password')
        serializer = self.serializer_class(data=request.data, 
                                           context={
                                               'owner': request.user,
                                               'confirm_password': confirm_password
                                            })

        if serializer.is_valid(raise_exception=True):
            course = serializer.save()
            serializer = self.serializer_class(instance=course)
            return Response(serializer.data, status=HTTP_201_CREATED)


class CourseListAPIView(APIView):
    queryset = Course.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseSerializer

    def get(self, request):
        owned_courses = Course.objects.filter(owner=request.user)
        joined_courses = request.user.courses.all()

        owned_serializer = self.serializer_class(instance=owned_courses, many=True)
        joined_serializer = self.serializer_class(instance=joined_courses, many=True)

        response = {
            'owned_courses': owned_serializer.data,
            'joined_courses': joined_serializer.data
        }

        return Response(response, status=HTTP_200_OK)


class CourseUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseUpdateSerializer
    
    def patch(self, request):
        course_id = request.data.get('id')
        message = get_course_id_error_message_if_any(course_id)
        
        if message:
            return Response(message, status=HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=int(course_id))

        if course.owner != request.user:
            return Response(status=HTTP_403_FORBIDDEN)
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            course = serializer.update(course, serializer.validated_data)
            return Response(CourseSerializer(instance=course).data, status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)


class JoinCourseAPIVIew(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        course_id = request.data.get('id')
        message = get_course_id_error_message_if_any(course_id)
        
        if message:
            return Response(message, status=HTTP_400_BAD_REQUEST)
        
        course = Course.objects.get(id=course_id)
        if course.users.contains(request.user):
            return Response(f'User {request.user} is already joined this course.', status=HTTP_403_FORBIDDEN)

        course.users.add(request.user)
        return Response(CourseSerializer(instance=course).data, status=HTTP_200_OK)


class LeaveCourseAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        course_id = request.data.get('id')
        message = get_course_id_error_message_if_any(course_id)
        
        if message:
            return Response(message, status=HTTP_400_BAD_REQUEST)

        course = Course.objects.get(id=course_id)
        if not course.users.contains(request.user):
            return Response(f'User {request.user} is not a member of this course.', status=HTTP_403_FORBIDDEN)
        
        course.users.remove(request.user)
        return Response(status=HTTP_200_OK)
