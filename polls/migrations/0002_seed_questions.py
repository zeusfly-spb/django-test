from django.db import migrations
from django.utils import timezone

QUESTIONS = [
    "Что такое Django ORM?",
    "Как подключить базу данных в Django?",
    "Как работают миграции?",
    "Как добавить сидер в Django?",
]


def seed(apps, schema_editor):
    Question = apps.get_model("polls", "Question")
    now = timezone.now()
    for text in QUESTIONS:
        Question.objects.get_or_create(
            question_text=text,
            defaults={"pub_date": now},
        )


def unseed(apps, schema_editor):
    Question = apps.get_model("polls", "Question")
    Question.objects.filter(question_text__in=QUESTIONS).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0001_initial"),
    ]
    operations = [
        migrations.RunPython(seed, unseed),
    ]
