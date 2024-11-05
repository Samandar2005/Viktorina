from django import forms
from .models import Quiz, Question


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'creator_name']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'correct_answer']
