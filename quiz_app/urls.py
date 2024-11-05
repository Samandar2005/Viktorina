from django.urls import path
from . import views

urlpatterns = [
    path('', views.enter_participant_name, name='enter_name'),  # Ism kiritish sahifasi
    path('create/<str:participant_name>/', views.create_quiz, name='create_quiz'),  # Viktorinani yaratish sahifasi
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),  # Viktorinani batafsil ko'rish sahifasi
    path('quiz/<int:quiz_id>/submit/', views.submit_answers, name='submit_answers'),  # Javoblarni yuborish sahifasi
    path('quiz/<int:quiz_id>/result/<str:participant_name>/', views.quiz_result, name='quiz_result'),  # Natijalarni ko'rish sahifasi
]
