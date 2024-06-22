from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT, HTTP_201_CREATED

from course.models import Course
from .serializers import TaskSerializer, UserTaskSerializer, UserTaskFileSerializer, OwnerTaskFileSerializer
from ..models import Task, OwnerTaskFile, UserTask, UserTaskFile


class TaskAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get(self, request):
        task_id = request.data.get('id')
        
        if not task_id:
            return Response('id is required', status=HTTP_400_BAD_REQUEST)

        try:
            task_id = int(task_id)
        except ValueError:
            return Response('id must be a number', status=HTTP_400_BAD_REQUEST)

        if not Task.objects.filter(id=task_id).exists():
            return Response(status=HTTP_404_NOT_FOUND)
        
        task = Task.objects.get(id=task_id)
        
        serializer = self.serializer_class(instance=task)
        return Response(serializer.data)

    def post(self, request):
        course_id = request.data.get('course_id')
        
        if not course_id:
            return Response('id is required', status=HTTP_400_BAD_REQUEST)
        
        try:
            course_id = int(course_id)
        except ValueError:
            return Response('id must be a number', status=HTTP_400_BAD_REQUEST)
        
        if not Course.objects.filter(id=course_id).exists():
            return Response(status=HTTP_404_NOT_FOUND)
        
        if Course.objects.get(id=course_id).owner != request.user:
            return Response(status=HTTP_403_FORBIDDEN)
        
        data = request.data.copy()
        data.update({'course': course_id})
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            task = serializer.save()
            return Response(self.serializer_class(instance=task).data)

        return Response(status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        task_id = request.data.get('task_id')
        
        if not task_id:
            return Response('id is required', status=HTTP_400_BAD_REQUEST)

        try:
            task_id = int(task_id)
        except ValueError:
            return Response('id must be a number', status=HTTP_400_BAD_REQUEST)

        if not Task.objects.filter(id=task_id).exists():
            return Response(status=HTTP_404_NOT_FOUND)
        
        task = Task.objects.get(id=task_id)

        if task.course.owner != request.user:
            return Response(status=HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(instance=task)
        task = task.delete()
        
        return Response(serializer.data, status=HTTP_204_NO_CONTENT)


class TaskListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    
    def get(self, request):
        course_id = request.data.get('course_id')
        
        if not course_id:
            return Response(status=HTTP_400_BAD_REQUEST)
        
        try:
            course_id = int(course_id)
        except ValueError:
            return Response(status=HTTP_400_BAD_REQUEST)
        
        if not Course.objects.filter(id=course_id).exists():
            return Response(status=HTTP_404_NOT_FOUND)
        
        course = Course.objects.get(id=course_id)
        serializer = self.serializer_class(instance=course.task_set.all(), many=True)
        
        return Response(serializer.data)


class OwnerFilesAPIView(APIView):
    parser_classes = (FileUploadParser, JSONParser)
    permission_classes = (IsAuthenticated,)
    serializer_class = OwnerTaskFileSerializer
    
    def get(self, request):
        task_id = request.data.get('task_id')
        
        if not task_id:
            return Response('id is required', status=HTTP_400_BAD_REQUEST)

        try:
            task_id = int(task_id)
        except ValueError:
            return Response('id must be a number', status=HTTP_400_BAD_REQUEST)

        if not Task.objects.filter(id=task_id).exists():
            return Response(status=HTTP_404_NOT_FOUND)
        
        task = Task.objects.get(id=task_id)
        task_files = OwnerTaskFile.objects.filter(task=task)
        serializer = self.serializer_class(instance=task_files, many=True)
        
        return Response(serializer.data)
    
    def post(self, request):
        files = request.FILES
        task_id = request.data.get('task_id')
        print(task_id)
        if not task_id:
            return Response('id is required', status=HTTP_400_BAD_REQUEST)

        try:
            task_id = int(task_id)
        except ValueError:
            return Response('id must be a number', status=HTTP_400_BAD_REQUEST)

        if not Task.objects.filter(id=task_id).exists():
            return Response(status=HTTP_404_NOT_FOUND)

        task = Task.objects.get(id=task_id)
        
        if task.course.owner != request.user:
            return Response(status=HTTP_403_FORBIDDEN)

        for file in files:
            data = {
                'owner': request.user.id,
                'media': file,
                'task': task.id
            }
            serializer = self.serializer_class(data=data)

            if not serializer.is_valid(raise_exception=True):
                return Response(status=HTTP_400_BAD_REQUEST)
            
            serializer.save()

        return Response(status=HTTP_201_CREATED)


class UserFilesAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserTaskFileSerializer
    
    def get(self, request):
        task_id = request.data.get('task_id')
        
        if not task_id:
            return Response('id is required', status=HTTP_400_BAD_REQUEST)

        try:
            task_id = int(task_id)
        except ValueError:
            return Response('id must be a number', status=HTTP_400_BAD_REQUEST)

        if not Task.objects.filter(id=task_id).exists():
            return Response(status=HTTP_404_NOT_FOUND)

        task = Task.objects.get(id=task_id)
        user_files = UserTaskFile.objects.filter(task=task, user=request.user)
        serializer = self.serializer_class(instance=user_files, many=True)
        
        return Response(serializer.data)
    
    def post(self, request):
        files = request.FILES.getlist('file')
        task_id = request.data.get('task_id')
        
        if not task_id:
            return Response(status=HTTP_400_BAD_REQUEST)

        try:
            task_id = int(task_id)
        except ValueError:
            return Response(status=HTTP_400_BAD_REQUEST)

        if not Task.objects.filter(id=task_id).exists():
            return Response(status=HTTP_404_NOT_FOUND)

        task = Task.objects.get(id=task_id)
        

        for file in files:
            data = {
                'user': request.user,
                'media': file,
                'task': task
            }
            serializer = self.serializer_class(data=data)
            serializer.save()

        return Response(status=HTTP_201_CREATED)
