# Generated by Django 4.2.4 on 2023-08-24 16:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={"verbose_name": "Article"},
        ),
    ]
