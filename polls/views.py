from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice



# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    return render(request, "polls/index.html", {"latest_question_list": latest_question_list})


def home(request):
    return render(request, "polls/home.html")

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            raise ValidationError({
                'refresh': 'Refresh token is required.'
            })

        try:
            token = RefreshToken(refresh_token)

            # Проверяем, что токен принадлежит текущему пользователю
            token_user_id = token.get(api_settings.USER_ID_CLAIM)

            if str(token_user_id) != str(request.user.pk):
                raise ValidationError({
                    'refresh': 'Token does not belong to this user.'
                })

            # Отзываем Refresh Token
            token.blacklist()

        except TokenError:
            raise ValidationError({
                'refresh': 'Invalid or expired refresh token.'
            })

        return Response(status=status.HTTP_205_RESET_CONTENT)
    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Получаем выбранный вариант из формы
        selected_choice = question.choices.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Если ничего не выбрали — возвращаем страницу вопроса с ошибкой
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "Вы не выбрали вариант ответа.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # После голосования перенаправляем на страницу результатов
        # return redirect("results", question_id=question.id)
        return redirect("polls:results", question_id=question.id)

    
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})



