from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Answer
from .forms import QuestionForm
import uuid
from django.http import JsonResponse
from django.urls import reverse
import json


def create_quiz(request):
    if request.method == 'POST':
        creator_name = request.POST.get('creator_name')
        if creator_name:
            quiz = Quiz.objects.create(creator_name=creator_name, link_id=str(uuid.uuid4()))
            return redirect('add_question', quiz_id=quiz.id)
    return render(request, 'create_quiz.html')


def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if quiz.questions.count() >= 10:
        return redirect('quiz_link', quiz_id=quiz.id)

    form = QuestionForm(request.POST or None)
    if form.is_valid():
        question = form.save(commit=False)
        question.quiz = quiz
        question.save()
        if quiz.questions.count() >= 10:
            return redirect('quiz_link', quiz_id=quiz.id)
        return redirect('add_question', quiz_id=quiz.id)

    return render(request, 'add_question.html', {'form': form, 'quiz': quiz})


def quiz_link(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    link = request.build_absolute_uri(reverse('take_quiz', args=[quiz.link_id]))
    return render(request, 'quiz_link.html', {'link': link})


def take_quiz(request, link_id):
    quiz = get_object_or_404(Quiz, link_id=link_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        data = json.loads(request.body)
        user_name = data.get('user_name')
        answers = data.get('answers', {})
        score = 0

        # Log the received answers for debugging
        print(f"User answers received: {answers}")

        # Calculate score based on correct answers
        for question in questions:
            user_answer = answers.get(f'question_{question.id}')
            correct_answer = 'True' if question.is_true else 'False'

            # Log each question and comparison result
            print(f"Question ID: {question.id}, User Answer: {user_answer}, Correct Answer: {correct_answer}")

            if str(user_answer) == correct_answer:  # Ensure both are strings for comparison
                score += 1

        # Log final score before saving
        print(f"Final calculated score: {score}")

        # Store or update the score in the database
        answer, created = Answer.objects.get_or_create(
            quiz=quiz,
            user_name=user_name,
            defaults={'score': score}
        )

        if not created:
            answer.score = score
            answer.save()

        # Redirect to the results page
        redirect_url = reverse('quiz_result', args=[quiz.id, user_name])
        return JsonResponse({'success': True, 'redirect_url': redirect_url})

    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})


def quiz_result(request, quiz_id, user_name):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    try:
        user_score = Answer.objects.get(quiz=quiz, user_name=user_name).score
        print(f"User score found: {user_score}")  # Debugging
    except Answer.DoesNotExist:
        user_score = None
        print(f"No score found for user: {user_name}")  # Debugging

    all_scores = Answer.objects.filter(quiz=quiz).order_by('-score')
    print(f"All scores: {[f'{a.user_name}: {a.score}' for a in all_scores]}")  # Debugging

    return render(request, 'quiz_result.html', {'user_score': user_score, 'all_scores': all_scores})
