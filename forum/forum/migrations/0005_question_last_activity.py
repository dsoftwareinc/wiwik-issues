# Generated by Django 4.1.3 on 2022-11-12 18:38

from django.db import migrations, models
from django.db.models import Max


def calculate_last_activity(apps, schema_editor):
    Question = apps.get_model("forum", "Question")
    for q in Question.objects.all():
        times = [
            q.created_at,
            q.status_updated_at,
        ]
        times.extend(q.comments.values_list("created_at", flat=True))
        times.extend(q.answer_set.values_list("updated_at", flat=True))
        times.extend(
            q.answer_set.annotate(last_comment=Max("comments__created_at")).values_list("last_comment", flat=True)
        )
        times = filter(lambda x: x is not None, times)
        q.last_activity = max(times)
        q.save()


def do_nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("forum", "0004_remove_questionadditionaldata_link_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="last_activity",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(calculate_last_activity, do_nothing),
    ]
