from operator import is_
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

from task.models import Task
from authentication.models import CustomUser


class Quiz(models.Model):
    
    task = models.ForeignKey(Task, on_delete=CASCADE)
    description = models.TextField(null=True)


class UserResult(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=CASCADE)


class Question(models.Model):
    
    quiz = models.ForeignKey(Quiz, on_delete=CASCADE)
    question = models.CharField(max_length=550)
    price = models.FloatField(default=0)
    text_answer = models.BooleanField(default=False)
    
    def create_question(self, quiz, question_text, price=0, text_answer=False, commit=True):
        self.quiz = quiz
        self.question_text = question_text
        self.text_answer = text_answer
        self.price = price
        
        if commit:
            self.save()
            
        return self


class Option(models.Model):
    
    question = models.ForeignKey(Question, on_delete=CASCADE)
    option = models.CharField(max_length=255)
    is_right = models.BooleanField(default=False)
    
    def create_question_option(self, question, option, is_right=False, commit=True):
        self.question = question
        self.option = option
        self.is_right = is_right
        
        if commit:
            self.save()
            
        return self

class ResultDetail(models.Model):
    
    user_result = models.ForeignKey(UserResult, on_delete=CASCADE)
    question = models.ForeignKey(Question, on_delete=CASCADE)
    option = models.ForeignKey(Option, on_delete=CASCADE, null=True, blank=True)
    is_right = models.BooleanField(null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)
