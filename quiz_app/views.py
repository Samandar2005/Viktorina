from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Answer
from .forms import QuizForm, QuestionForm
from django.db.models import Sum, Count


def create_quiz(request):
    if request.method == "POST":
        quiz_form = QuizForm(request.POST)
        question_formset = [QuestionForm(request.POST, prefix=str(i)) for i in range(10)]  # 10 ta savol uchun form
        if quiz_form.is_valid() and all(q_form.is_valid() for q_form in question_formset):
            quiz = quiz_form.save()
            for q_form in question_formset:
                question = q_form.save(commit=False)
                question.quiz = quiz
                question.save()
            return redirect('quiz_detail', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm()
        question_formset = [QuestionForm(prefix=str(i)) for i in range(10)]
    return render(request, 'create_quiz.html', {'quiz_form': quiz_form, 'question_formset': question_formset})


def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz_detail.html', {'quiz': quiz})


def submit_answers(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == "POST":
        participant_name = request.POST.get('participant_name')
        for question in quiz.questions.all():
            answer = request.POST.get(f'question_{question.id}')
            is_correct = (answer == 'True') == question.correct_answer
            Answer.objects.create(
                question=question,
                participant_name=participant_name,
                is_correct=is_correct
            )
        return redirect('quiz_result', quiz_id=quiz.id, participant_name=participant_name)
    return render(request, 'quiz_detail.html', {'quiz': quiz})


def quiz_result(request, quiz_id, participant_name):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    answers = Answer.objects.filter(question__quiz=quiz)
    participant_answers = answers.filter(participant_name=participant_name)
    correct_count = participant_answers.filter(is_correct=True).count()
    total_questions = quiz.questions.count()
    score = (correct_count / total_questions) * 100
    return render(request, 'quiz_result.html', {
        'quiz': quiz,
        'score': score,
        'participant_name': participant_name,
        'participant_answers': participant_answers,
        'all_answers': answers,
    })
