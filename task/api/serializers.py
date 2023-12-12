from rest_framework import serializers

from ..models import Task, UserTaskFile, UserTask, OwnerTaskFile


class UserTaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTaskFile
        fields = ['user', 'task', 'media', 'done_at', 'too_late']
        extra_kwargs = {
            'done_at': {'read_only': True}
        }


class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        fields = ['user', 'task', 'is_examined', 'mark', 'done_at']
        extra_kwargs = {
            'done_at': {'read_only': True}
        }


class  OwnerTaskFileSerializer(serializers.ModelSerializer):
    class Meta:
            model = OwnerTaskFile
            fields = ['owner', 'task', 'media']


class TaskSerializer(serializers.ModelSerializer):
    files = OwnerTaskFileSerializer(read_only=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'name', 'course', 'max_mark', 'description', 'do_up_to', 'created_at', 'files']
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True}
        }
