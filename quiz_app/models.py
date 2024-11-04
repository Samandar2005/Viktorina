from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    creator_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    correct_answer = models.BooleanField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    participant_name = models.CharField(max_length=50)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.participant_name} - {self.question.text}"
