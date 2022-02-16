from django import forms

from .models import Quiz, Question


class QuestionForm(forms.Form):
    quiz = forms.IntegerField()
    question = forms.CharField(required=True)
    is_textonly = forms.BooleanField(widget=forms.widgets.CheckboxInput(), required=False)

class OptionForm(forms.Form):
    question = forms.IntegerField()
    option = forms.CharField(required=True)
    is_right = forms.BooleanField(required=False)
