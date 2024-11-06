from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_quiz, name='create_quiz'),
    path('add-question/<int:quiz_id>/', views.add_question, name='add_question'),
    path('quiz-link/<int:quiz_id>/', views.quiz_link, name='quiz_link'),
    path('take-quiz/<str:link_id>/', views.take_quiz, name='take_quiz'),
    path('quiz-result/<int:quiz_id>/<str:user_name>/', views.quiz_result, name='quiz_result'),
]
