from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Quiz, Question, Answer
from .forms import QuizForm, QuestionForm
from django.db.models import Count


def enter_participant_name(request):
    # Step 1: User enters their name before creating a quiz
    if request.method == "POST":
        participant_name = request.POST.get('participant_name')
        return redirect('create_quiz', participant_name=participant_name)
    return render(request, 'enter_name.html')


def create_quiz(request, participant_name):
    # Create a quiz and add questions sequentially
    quiz, created = Quiz.objects.get_or_create(
        creator_name=participant_name,
        defaults={'title': 'Untitled Quiz'}
    )

    if request.method == "POST":
        question_form = QuestionForm(request.POST)

        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()

            # If fewer than 10 questions, allow adding another question
            if quiz.questions.count() < 10:
                return render(request, 'create_quiz.html', {
                    'question_form': QuestionForm(),
                    'quiz': quiz
                })
            # If 10 questions, redirect to the quiz detail page with generated URL
            return redirect('quiz_detail', quiz_id=quiz.id)
    else:
        question_form = QuestionForm()

    return render(request, 'create_quiz.html', {
        'question_form': question_form,
        'quiz': quiz
    })


def quiz_detail(request, quiz_id):
    # Display the quiz for participants to answer questions
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz_detail.html', {'quiz': quiz})


def submit_answers(request, quiz_id):
    # Participants submit answers for the quiz
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
    # Show results for the participant
    quiz = get_object_or_404(Quiz, id=quiz_id)
    participant_answers = Answer.objects.filter(question__quiz=quiz, participant_name=participant_name)
    correct_count = participant_answers.filter(is_correct=True).count()
    total_questions = quiz.questions.count()
    score = (correct_count / total_questions) * 100

    return render(request, 'quiz_result.html', {
        'quiz': quiz,
        'score': score,
        'participant_name': participant_name,
        'participant_answers': participant_answers,
    })
