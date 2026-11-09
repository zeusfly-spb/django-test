from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    return HttpResponse("Hello, world. You're at the polls home.")

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

