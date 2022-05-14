from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from task.models import Task
from authentication.models import CustomUser
from course.models import Course, UserCourse
from homepage.side_functions import context_add_courses

from .models import Quiz, Question, Option, ResultDetail, UserResult


class QuizCreateView(View):
    
    template_name = 'quiz/create.html'
    model = Quiz
    
    def get(self, request, course_id, task_id):
        try:
            if Quiz.objects.get(task=task_id):
                return redirect(f'/course/{course_id}/task/{task_id}/')
        except ObjectDoesNotExist:
            pass
            
        task = get_object_or_404(Task, id=task_id)
        context = {
            'task': task
        }
        context = context_add_courses(context, request.user)
        
        return render(request, self.template_name, context)
    
    def post(self, request, course_id, task_id):
        task = get_object_or_404(Task, id=task_id)
        
        try:
            Quiz.objects.get(task=task)
            return redirect(f'/course/{course_id}/task/{task_id}/')
        except:
            pass
        
        quiz = self.model.objects.create(task=task)
        
        question_start = 'question_'
        text_answer_start = 'textOnlyFor_'
        option_start = 'optionForQuestion_'
        option_value_start = 'optionValueForQuestion_'
        price_start = 'price_'
        question_counter = 1
        
        for name in request.POST.keys():
            if name.startswith(question_start):
                question_counter += 1
        
        for i in range(1, question_counter):
            question = Question()
            question.quiz = quiz
            question.question = request.POST.get(f'{question_start}{i}')
            question.text_answer = bool(request.POST.get(f'{text_answer_start}{i}'))
            question.price = request.POST.get(f'{price_start}{i}')
            question.save()
            
            option_counter = 1
            for name in request.POST.keys():
                if name.startswith(f'{option_start}{i}'):
                    option_counter += 1
            
            for j in range(1, option_counter):
                option = Option()
                option.option = request.POST.get(f'{option_start}{i}_{j}')
                option.is_right = bool(request.POST.get(f'{option_value_start}{i}_{j}'))
                option.question = question
                option.save()
        
        return redirect(f'/course/{course_id}/task/{task_id}')


class QuizDetailView(View):
    
    model = Quiz
    template_name = 'quiz/detail.html'
    
    def get(self, request, course_id, task_id):
        is_ready = False
        if request.GET.get('ready'):
            is_ready = True
        
        quiz = self.model.objects.get(task=task_id)
        questions = Question.objects.filter(quiz=quiz.id)
        course = Course.objects.get(id=course_id)
        users_course = UserCourse.objects.filter(course=course_id)
        options = []
        one_answer_questions = []
        users_done = []
        users_not_done = []
        
        for question in questions:
            current_options = Option.objects.filter(question=question.id)
            options.extend(current_options)
            
            counter = 0
            for option in current_options:
                if option.is_right:
                    counter += 1
            
            if counter > 1:
                one_answer_questions.append(question.id)
        
        for user_course in users_course:
            try:
                users_done.append(UserResult.objects.get(user=user_course.user).user)
            except ObjectDoesNotExist:
                users_not_done.append(user_course.user)
        
        context = {
            'quiz': quiz,
            'questions': questions,
            'one_answer_questions': one_answer_questions,
            'options': options,
            'is_ready': is_ready,
            'course_id': course_id,
            'task_id': task_id,
            'is_owner': course.owner == request.user,
            'users_done': users_done,
            'users_not_done': users_not_done
        }
        context = context_add_courses(context, request.user)
        
        return render(request, self.template_name, context)
    
    def post(self, request, course_id, task_id):
        option_start = 'option_'
        text_start = 'describe_'
        quiz = Quiz.objects.get(task=task_id)
        user_result = UserResult.objects.create(user=request.user, quiz=quiz)
        
        for name in request.POST.keys():
            if name.startswith(option_start):
                option_id = int(name[name.find('_') + 1:])
                option = Option.objects.get(id=option_id)
                result_detail = ResultDetail.objects.create(user_result=user_result, question=option.question, option=option, is_right=option.is_right)
                result_detail.save()
            elif name.startswith(text_start):
                question_id = int(name[name.find('_') + 1:])
                question = Question.objects.get(id=question_id)
                text_anser = request.POST.get(name)
                result_detail = ResultDetail.objects.create(user_result=user_result, question=question, text_answer=text_anser)
                result_detail.save()
        
        return redirect('/')


class UserDetailView(View):
    
    model = Quiz
    template_name = 'quiz/user-detail.html'
    
    def get(self, request, course_id, task_id, user_id):
        user = CustomUser.objects.get(id=user_id)
        task = Task.objects.get(id=task_id)
        quiz = Quiz.objects.get(task=task)
        user_result = UserResult.objects.get(user=user, quiz=quiz)
        user_results = ResultDetail.objects.filter(user_result=user_result)
        questions = Question.objects.filter(quiz=quiz)
        options = []
        
        for q in questions:
            options.extend(Option.objects.filter(question=q))
        
        context = {
            'user_results': user_results,
            'questions': questions,
            'options': options,
            'final_mark': self.analyse_answers(questions, options, user_results)
        }
        context = context_add_courses(context, request.user)
        
        return render(request, self.template_name, context)

    def analyse_answers(self, questions, options, user_results):
        def right_answers(options, question):
            counter = 0
            for option in options:
                if option.question == question and option.is_right:
                    counter += 1
                    
            return counter
        
        final_mark = 0
        
        for question in questions:
            counter = 0
            true_answers = right_answers(options, question)
            
            for result in user_results:
                if result.question == question and result.is_right:
                    counter += 1
                    print('true')
                print(result.is_right)
            print(counter)
            if question.price != 0:
                one_aswer_value = true_answers / question.price
                final_mark += counter * one_aswer_value
        
        return final_mark
                    
