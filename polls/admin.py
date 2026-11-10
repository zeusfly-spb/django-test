from django.contrib import admin
from .models import Question, Choice
from django.utils import timezone
import datetime

class ChoiceInline(admin.TabularInline):
    """
    Табличный вид встроенных вариантов: по одной строке на вариант.
    Можно поменять на admin.StackedInline, если хочется «карточки» вместо таблицы.
    """
    model = Choice
    extra = 3  # сколько пустых строк показывать сразу при создании нового вопроса
    min_num = 1  # минимум один вариант обязателен (опционально)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ("pub_date",)
    search_fields = ("question_text",)
    inlines = [ChoiceInline]  # вот тут подключаем встроенные варианты



@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "votes")
    search_fields = ("choice_text",)
