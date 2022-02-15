from django.core.exceptions import ObjectDoesNotExist
from django import views
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from task.models import Task
from .models import Quiz, Question, Option


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
        return render(request, self.template_name, context)
    
    def post(self, request, course_id, task_id):
        task = get_object_or_404(Task, id=task_id)
        self.model = self.model()
        self.model.task = task
        self.model.save()
        
        question_start = 'question_'
        text_answer_start = 'textOnlyFor_'
        option_start = 'optionForQuestion_'
        option_value_start = 'optionValueForQuestion_'
        question_counter = 1
        
        for name in request.POST.keys():
            if name.startswith(question_start):
                question_counter += 1
        
        for i in range(1, question_counter):
            question = Question()
            question.quiz = self.model
            question.question = request.POST.get(f'{question_start}{i}')
            question.text_answer = bool(request.POST.get(f'{text_answer_start}{i}'))
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
        # task = get_object_or_404(Task, task_id)
        is_ready = False
        if request.GET.get('ready'):
            is_ready = True
        
        quiz = self.model.objects.get(task=task_id)
        questions = Question.objects.filter(quiz=quiz.id)
        options = []
        
        for question in questions:
            options.extend(Option.objects.filter(question=question.id))
        
        context = {
            'quiz': quiz,
            'questions': questions,
            'options': options,
            'is_ready': is_ready,
            'course_id': course_id,
            'task_id': task_id
        }
        return render(request, self.template_name, context)
    
    
# TODO: 
# Quiz show in TaskDetailView. 
# Quiz detail. 
# Quiz update. 
# Quiz delete. 
# Make only 1 quiz possible for 1 task.
# UserResult for Quiz.
# View UserResults for Course Admin
