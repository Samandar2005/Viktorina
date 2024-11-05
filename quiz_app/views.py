from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Answer
from .forms import QuizForm, QuestionForm
from django.db.models import Count


def enter_participant_name(request):
    # Foydalanuvchi ismini kiritish sahifasi
    if request.method == "POST":
        participant_name = request.POST.get('participant_name')
        return redirect('create_quiz', participant_name=participant_name)
    return render(request, 'enter_name.html')


def create_quiz(request, participant_name):
    # Viktorinani yaratish va savollarni ketma-ket kiritish sahifasi
    if request.method == "POST":
        quiz_form = QuizForm(request.POST)
        question_form = QuestionForm(request.POST)

        if quiz_form.is_valid() and question_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.creator_name = participant_name
            quiz.save()

            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()

            # Agar savollar soni hali 10 taga yetmagan bo'lsa, yangi savol kiritishni davom ettiradi
            if quiz.questions.count() < 10:
                return render(request, 'create_quiz.html', {
                    'quiz_form': quiz_form,
                    'question_form': QuestionForm(),
                    'quiz': quiz
                })
            # 10 ta savol to'ldirilganda batafsil sahifaga o'tadi
            return redirect('quiz_detail', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm()
        question_form = QuestionForm()

    return render(request, 'create_quiz.html', {
        'quiz_form': quiz_form,
        'question_form': question_form,
    })


def quiz_detail(request, quiz_id):
    # Viktorinani batafsil ko'rish va javoblarni yuborish sahifasi
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz_detail.html', {'quiz': quiz})


def submit_answers(request, quiz_id):
    # Foydalanuvchi javoblarini yuboradi va natijalarni hisoblaydi
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
    # Ishtirokchining natijalarini ko'rsatish sahifasi
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
