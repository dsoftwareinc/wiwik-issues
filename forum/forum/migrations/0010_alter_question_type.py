# Generated by Django 4.2.5 on 2023-09-14 13:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forum", "0009_rename_questioninvitetoanswer_postinvitation_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="type",
            field=models.CharField(
                choices=[("a", "Article"), ("q", "Question"), ("h", "How to")],
                default="q",
                help_text="Post type",
                max_length=2,
            ),
        ),
    ]
