from django.db import models


class Quiz(models.Model):
    creator_name = models.CharField(max_length=50)
    link_id = models.CharField(max_length=100, unique=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Quiz by {self.creator_name}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_true = models.BooleanField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user_name} - {self.score} points"
