from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'is_true']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Savol matni...'}),
            'is_true': forms.RadioSelect(choices=[(True, 'Rost'), (False, 'Yolg‘on')])
        }
