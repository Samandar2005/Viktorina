from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_quiz, name='create_quiz'),  # Viktorinani yaratish sahifasi
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),  # Link orqali kirganlar uchun sahifa
    path('quiz/<int:quiz_id>/submit/', views.submit_answers, name='submit_answers'),  # Javoblarni yuborish uchun
    path('quiz/<int:quiz_id>/result/<str:participant_name>/', views.quiz_result, name='quiz_result'),

]
