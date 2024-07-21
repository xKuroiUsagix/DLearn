from rest_framework import serializers

from ..models import Quiz, Question, Option, ResultDetail, UserResult


class ResultDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultDetail
        fields = ['user_result', 'question', 'option', 'mark', 'is_right', 'text_answer']


class UserResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResult
        fields = ['id', 'user', 'quiz', 'mark']
        extra_kwargs = {
            'id': {'read_only': True}
        }


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'question', 'option', 'is_right']
        extra_kwargs = {
            'id': {'read_only': True}
        }
    
    def validate(self, data):
        question = data.get('question')
        
        if not question:
            raise serializers.ValidationError('`question` should be provided')
        if question.text_answer:
            raise serializers.ValidationError('Can not add an option for question with text answer.')
        
        return super().validate(data)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['quiz', 'question', 'price', 'text_answer']
    
    def to_representation(self, instance):
        options = OptionSerializer(instance=instance.get_options(), many=True).data

        data = {
            'id': instance.id,
            'quiz': instance.quiz.id,
            'question': instance.question,
            'price': instance.price,
            'text_answer': instance.text_answer,
            'options': options
        }
        return data


class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = ['id', 'description', 'task']
        extra_kwargs = {
            'id': {'read_only': True}
        }
    
    def to_representation(self, instance):
        questions = QuestionSerializer(instance=instance.get_questions(), many=True).data
        data = {
            'id': instance.id,
            'task': instance.task.id,
            'description': instance.description,
            'questions': questions
        }
        return data
