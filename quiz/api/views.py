from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_403_FORBIDDEN

from .serializers import QuizSerializer, QuestionSerializer, OptionSerializer, UserResultSerializer, ResultDetailSerializer
from ..models import Quiz, Option, Question, UserResult, ResultDetail


def count_mark_for_question(question, selected_options):
    right_options, false_options = 0, 0
    right_selected_options, false_selected_options = 0, 0
    
    for option in question.get_options():
        if option.is_right:
            right_options += 1
        else:
            false_options += 1
    
    for option in selected_options:
        if option.is_right:
            right_selected_options += 1
        else:
            false_selected_options += 1
    
    right_percent = right_selected_options / right_options
    false_percent = false_selected_options / false_options
    
    mark = round(question.price * (right_percent - false_percent))
    return mark if mark > 0 else 0


class QuizAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuizSerializer

    def get(self, request):
        quiz = get_object_or_404(Quiz, id=request.data['quiz_id'])
        serializer = self.serializer_class(instance=quiz)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            quiz = serializer.save()
            return Response(self.serializer_class(instance=quiz).data, status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pass


class QuestionAPIVIew(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializer
    
    def get(self, request):
        question = get_object_or_404(Question, id=request.data['id'])
        serializer = self.serializer_class(instance=question)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            question = serializer.save()
            return Response(self.serializer_class(instance=question).data, status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)


class OptionAPiView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OptionSerializer
    
    def get(self, request):
        option = get_object_or_404(Option, id=request.data['id'])
        serializer = self.serializer_class(instance=option)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            option = serializer.save()
            return Response(self.serializer_class(instance=option).data, status=HTTP_201_CREATED)

        return Response(status=HTTP_400_BAD_REQUEST)


class StartQuizAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserResultSerializer
    
    def post(self, request):
        data = request.data.copy()
        data.update({'user': request.user.id})
        serializer = self.serializer_class(data=data)

        if UserResult.objects.filter(user=data['user'], quiz=data['quiz']).exists():
            return Response('This user is already started this quiz.', status=HTTP_403_FORBIDDEN)
        
        if serializer.is_valid(raise_exception=True):
            user_result = serializer.save()
            return Response(self.serializer_class(instance=user_result).data, status=HTTP_201_CREATED)


class UserResultAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserResultSerializer
    
    def get(self, request):
        user_result = get_object_or_404(UserResult, user=request.data.get('user'), quiz=request.data.get('quiz'))
        serializer = self.serializer_class(instance=user_result)
        return Response(serializer.data)


class QuestionSelectOptionsAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResultDetailSerializer
    
    def post(self, request):
        user_result = get_object_or_404(UserResult, id=request.data.get('user_result'))
        question = get_object_or_404(Question, id=request.data.get('question'))
        options = []
        
        for option in request.data.get('options'):
            options.append(get_object_or_404(Option, id=option))
            
            if options[-1] not in question.get_options():
                return Response(f'There is no such option for Question[{question.id}]', status=HTTP_400_BAD_REQUEST)
        
        for option in options:
            data = {
                'user_result': user_result.id,
                'question': question.id,
                'option': option.id,
                'mark': count_mark_for_question(question, options),
                'is_right': option.is_right
            }
            serializer = self.serializer_class(data=data)
            
            if not serializer.is_valid(raise_exception=True):
                serializer.save()
        
        return Response(status=HTTP_201_CREATED)


class QuestionAddTextAnswer(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResultDetailSerializer
    
    def post(self, request):
        user_result = get_object_or_404(UserResult, id=request.data.get('user_result'))
        question = get_object_or_404(Question, id=request.data.get('question'))
        text_answer = request.data.get('text_answer')
        
        if not question.text_answer:
            return Response('Question[{question.id}] can not has text answer.', status=HTTP_400_BAD_REQUEST)
        if not text_answer:
            return Response('Text answer can not be Null.', status=HTTP_400_BAD_REQUEST)
        
        data = {
            'user_result': user_result.id,
            'question': question.id,
            'text_answer': text_answer
        }
        
        serializer = self.serializer_class(data=data)
        
        if not serializer.is_valid(raise_exception=True):
            return Response(status=HTTP_400_BAD_REQUEST)
            
        serializer.save()
        return Response(status=HTTP_201_CREATED)
    

class QuestionSetMark(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResultDetailSerializer
    
    def put(self, request):
        user_result = get_object_or_404(UserResult, id=request.data.get('user_result'))
        result_detail = get_object_or_404(ResultDetail, user_result=user_result, question=request.data.get('question'))
        mark = request.data.get('mark')
        
        if result_detail.text_answer is None:
            return Response('You can not set a mark for user they did not give an answer.', status=HTTP_400_BAD_REQUEST)
        
        try:
            mark = int(mark)
        except ValueError:
            return Response('Mark must be an integer.', status=HTTP_400_BAD_REQUEST)

        if mark < 0 or mark > result_detail.question.price:
            return Response(f'Mark can not be negative or higher than question max mark ({result_detail.question.price})', status=HTTP_400_BAD_REQUEST)
        
        result_detail.mark = mark
        result_detail.save()
        return Response(status=HTTP_200_OK)


class CountMarkForQuiz(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserResultSerializer
    
    def post(self, request):
        user_result = get_object_or_404(UserResult, id=request.data.get('user_result'))
        result_detail = ResultDetail.objects.filter(user_result=user_result)
        
        unique_questions = result_detail.order_by().values('question').distinct()
        total_mark = 0

        for record in unique_questions:
            result = ResultDetail.objects.filter(question=record.get('question'))[0]
            total_mark += result.mark
        
        user_result.mark = total_mark
        user_result.save()
        
        serializer = self.serializer_class(instance=user_result)

        return Response(serializer.data)


class ResultDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResultDetailSerializer
    
    def get(self, request):
        user_result = request.data.get('user_result')
        results = get_list_or_404(ResultDetail, user_result=user_result)
        
        serializer = self.serializer_class(instance=results, many=True)
        
        return Response(serializer.data)
