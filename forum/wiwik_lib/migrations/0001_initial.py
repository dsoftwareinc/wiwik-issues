# Generated by Django 4.2 on 2023-04-29 17:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag_type', models.CharField(choices=[('rude', 'Rude'), ('spam', 'Spam'), ('moderator', 'Requires intervention'), ('close', 'Should be closed'), ('duplicate', 'Duplicate')], max_length=10)),
                ('extra', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='flags_for_user', to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flags_by_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EditedResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_ping_at', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_editing', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
