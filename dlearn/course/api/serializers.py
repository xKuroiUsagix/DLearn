from rest_framework import serializers

from ..models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'users', 'group_name', 'join_code', 'image', 'password']
        depth = 1
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        course = Course(
            name=validated_data['name'],
            group_name=validated_data['group_name'],
            join_code=validated_data['join_code'],
            image=validated_data['image'],
            owner=self.context['owner']
        )
        course.set_password(validated_data['password'])
        course.save()
        return course
    
    def validate(self, data):
        if data['password'] != self.context['confirm_password'][0]:
            msg = 'Password and confirm_password don\'t match.'
            raise serializers.ValidationError(msg)
        if Course.objects.filter(join_code=data['join_code']).exists():
            msg = 'This join code already exists.'
            raise serializers.ValidationError(msg)
        return data


class CourseUpdateSerializer(serializers.ModelSerializer):
    join_code = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = Course
        fields = ['name', 'group_name', 'join_code', 'image', 'password']
    
    def update(self, instance, validated_data):
        name = validated_data.get('name')
        join_code = validated_data.get('join_code')
        group_name = validated_data.get('group_name')
        image = validated_data.get('image')
        password = validated_data.get('password')
        confirm_password = validated_data.get('confirm_password')
        
        if name and name != instance.name:
            instance.name = name
        if join_code and join_code != instance.join_code:
            instance.join_code = join_code
        if group_name and group_name != instance.group_name:
            instance.group_name = group_name
        if image and image != instance.image:
            instance.image = image
        
        if password and confirm_password:
            instance.set_password(password)

        instance.save()
        return instance
    
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        join_code = data.get('join_code')

        if password:
            if password != confirm_password:
                msg = 'Password and confirm_password don\'t match.'
                raise serializers.ValidationError(msg)
        if join_code:
            if Course.objects.filter(join_code=data['join_code']).exists():
                msg = 'This join code already exists.'
                raise serializers.ValidationError(msg)

        return data
