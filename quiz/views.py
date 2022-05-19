import queue
from unittest import result
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from task.models import Task
from authentication.models import CustomUser
from course.models import Course, UserCourse
from homepage.side_functions import context_add_courses

from .models import Quiz, Question, Option, ResultDetail, UserResult


class QuizCreateView(View):
    """
        QuizCreateView provides operations for course owner to create quiz for task.
        
        Attributes:
        ----------
        param template_name: Describes html template for Quiz get view
        type template_name: str
        param model: Describes the Quiz model in database
        type model: Quiz
    """
    template_name = 'quiz/create.html'
    model = Quiz
    
    def get(self, request, course_id, task_id):
        if self.model.objects.filter(task=task_id):
            return redirect(f'/course/{course_id}/task/{task_id}/')
            
        task = get_object_or_404(Task, id=task_id)
        context = {
            'task': task
        }
        context = context_add_courses(context, request.user)
        
        return render(request, self.template_name, context)
    
    def post(self, request, course_id, task_id):
        task = get_object_or_404(Task, id=task_id)
        
        if self.model.objects.filter(task=task):
            return redirect(f'/course/{course_id}/task/{task_id}/')
        
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
            question = Question.objects.create (
                quiz=quiz,
                question=request.POST.get(f'{question_start}{i}'),
                text_answer=bool(request.POST.get(f'{text_answer_start}{i}')),
                price=request.POST.get(f'{price_start}{i}')
            )
            
            option_counter = 1
            for name in request.POST.keys():
                if name.startswith(f'{option_start}{i}'):
                    option_counter += 1
            
            for j in range(1, option_counter):
                Option.objects.create(
                    option=request.POST.get(f'{option_start}{i}_{j}'),
                    is_right=bool(request.POST.get(f'{option_value_start}{i}_{j}')),
                    question=question
                )
        
        return redirect(f'/course/{course_id}/task/{task_id}')


class QuizDetailView(View):
    """
    QuizDetailView has functionality for users to take quizes
    
    Attributes:
        ----------
        param template_name: Describes html file for detail
        type template_name: str
        param model: Describes the Quiz model in database
        type model: Quiz
    """
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
        users = [user_course.user for user_course in users_course]
        options, users_done, users_not_done, one_answer_questions = [], [], [], []
        
        if UserResult.objects.filter(user=request.user, quiz=quiz):
            return redirect(f'/course/{course_id}/task/{task_id}/quiz/user-detail/{request.user.id}/')
        
        for question in questions:
            current_options = Option.objects.filter(question=question.id)
            options.extend(current_options)
            
            if not self.is_question_one_optioned(question):
                continue
            one_answer_questions.append(question)
        
        for user in users:
            try:
                users_done.append(UserResult.objects.get(user=user, quiz=quiz).user)
            except ObjectDoesNotExist:
                users_not_done.append(user)
        
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
        quiz = self.model.objects.get(task=task_id)
        user_result = UserResult.objects.create(user=request.user, quiz=quiz)
        
        for name in request.POST.keys():                
            if name.startswith(option_start):
                option_id = int(name[name.find('_') + 1:]) # Getting option_id from strings like: "optionName_{option_id}"
                option = Option.objects.get(id=option_id)
            
                ResultDetail.objects.create(
                    user_result=user_result,
                    question=option.question,
                    option=option,
                    is_right=option.is_right
                )
            elif name.startswith(text_start):
                question_id = int(name[name.find('_') + 1:]) # Getting question_id from strings like: "questionName_{question_id}"
                question = Question.objects.get(id=question_id)
                text_answer = request.POST.get(name)
                
                ResultDetail.objects.create(
                    user_result=user_result,
                    question=question,
                    text_answer=text_answer
                )
        
        questions = Question.objects.filter(quiz=quiz, text_answer=False)
        options = []
        
        for question in questions:
            options.extend(Option.objects.filter(question=question))
        
        result_detail = ResultDetail.objects.filter(user_result=user_result)
        self.set_questions_marks(questions, options, result_detail)
        
        return redirect('/')
    
    def is_question_one_optioned(self, question):
        """This method checks each question's option and tells has it only one true asnwer or not.

        Args:
            question (Question): an object of Question class

        Returns:
            bool: whether question has only one option or more
        """
        options = Option.objects.filter(question=question)
        true_options_counter = 0
        
        for option in options:
            if option.is_right:
                true_options_counter += 1
        
        return true_options_counter == 1
                
    
    def set_questions_marks(self, questions, options, result_detail):
        """
        This function analyse each question, option and result_detail
        taken from user, then calculates mark for each question and set it to
        result mark field.
        
        How does mark calculation made:
            For each question function counts all true and false options
            Then calculates all true and false options which user done
            After this, we have true_percent and false_percent which calculated as:
                true_percent = user_true_options / all_true_options
                false_percent = user_false_options / all_false_options
            Then from true_percent substracts false_percents, and result multiplies to question price
            
            For example:
                if user choose all options in question:
                    false_percent equals 1, and true_percent equals 1
                    which means that ture_percent - false_percent equals 0
                    so question mark will be 0
                
                if user choose 1 true option, 1 false option, and 1 option will be untoched (1 true option at all):
                    false_percent equals 0.5, and true_percent equals 1
                    which means that true_percent - false_percent equals 0.5
                    so question mark will be a half of question price

        Args:
            questions (list): All Questions from Quiz
            options (list): All Options from Quiz
            result_detail (ResultDetail): All ResultDetail for certain user which has done the quiz
        """
        for question in questions:
            true_options, false_options = 0, 0
            u_true_options, u_false_options = 0, 0
            
            for option in options:
                if option.question == question:
                    if option.is_right:
                        true_options += 1
                    else:
                        false_options += 1
            
            for result in result_detail:
                if result.question == question:
                    if result.is_right:
                        u_true_options += 1
                    else:
                        u_false_options += 1
            
            true_percent = u_true_options / true_options
            false_percent = u_false_options / false_options
            
            for result in result_detail:
                if result.question == question:
                    mark = round(question.price * (true_percent - false_percent))
                    result.mark = mark if mark > 0 else 0
                    result.save()


class UserDetailView(View):
    """
        UserDetailView provides operations for owner to see each user task results.
        
        Attributes:
        ----------
        param template_name: Describes html template for user-detail
        type model: str
        param model: Describes the Quiz model in database
        type model: Quiz
    """
    model = Quiz
    template_name = 'quiz/user-detail.html'
    
    def get(self, request, course_id, task_id, user_id):
        user = CustomUser.objects.get(id=user_id)
        task = Task.objects.get(id=task_id)
        quiz = self.model.objects.get(task=task)
        user_result = UserResult.objects.get(user=user, quiz=quiz)
        result_details = ResultDetail.objects.filter(user_result=user_result)
        questions = Question.objects.filter(quiz=quiz)
        options = []
        
        user_result.mark = self.count_mark(result_details)
        user_result.save()
        
        for q in questions:
            options.extend(Option.objects.filter(question=q))
        
        context = {
            'user': user,
            'is_owner': Course.objects.get(id=course_id).owner == request.user,
            'task_id': task_id,
            'course_id': course_id, 
            'result_details': result_details,
            'questions': questions,
            'options': options,
            'final_mark': user_result.mark
        }
        context = context_add_courses(context, request.user)
        
        return render(request, self.template_name, context)
    
    def post(self, request, course_id, task_id, user_id):
        task_start = 'descriptionTask_'
        
        for name in request.POST.keys():
            if name.startswith(task_start):
                question_id = int(name[name.find('_') + 1:])
                question = Question.objects.get(id=question_id)
                
                task = Task.objects.get(id=task_id)
                quiz = Quiz.objects.get(task=task)
                user = CustomUser.objects.get(id=user_id)
                user_result = UserResult.objects.get(quiz=quiz, user=user)
                
                result_detail = ResultDetail.objects.get(user_result=user_result, question=question)
                result_detail.mark = int(request.POST[name])
                result_detail.save()
        
        return redirect(f'/course/{course_id}/task/{task_id}/quiz/user-detail/{user_id}')
    
    def count_mark(self, result_details):
        """This method counts the quiz marks summary.

        Args:
            result_details (list): List of ResultDetail class objects

        Returns:
            int: final mark for user in quiz
        """
        previous_questions = set()
        mark = 0
        
        for result in result_details:
            if result.question in previous_questions:
                continue
            
            mark += result.mark
            previous_questions.add(result.question)
            
        return mark
