# Generated by Django 4.0.6 on 2022-07-31 16:39

import django.contrib.postgres.indexes
import django.contrib.postgres.search
import django.utils.timezone
from django.conf import settings
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import SearchVector
from django.db import migrations, models
from django.db.models import TextField


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# forum.migrations.0001_squashed_0007_questionview
# forum.migrations.0002_auto_20220104_1426


def forwards(apps, schema_editor):
    if not schema_editor.connection.vendor.startswith("postgres"):
        return
    try:
        schema_editor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    except Exception as e:
        print(e)


def populate_search_vector(apps, schema_editor):
    if not schema_editor.connection.vendor.startswith("postgres"):
        return
    question_model = apps.get_model("forum", "Question")
    vector = (
        SearchVector("title", weight="A")
        + SearchVector("content", weight="B")
        + SearchVector(StringAgg("tags__tag_word", delimiter=","), weight="B")
        + SearchVector(
            StringAgg("answer__content", delimiter="\n", output_field=TextField()),
            weight="D",
        )
    )
    qs = question_model.objects.annotate(document=vector).all()
    for q in qs:
        q.additional_data.search_vector = q.document
        q.additional_data.save()


def do_nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("badges", "0001_squashed_0003_auto_20211211_1535"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("tags", "0001_initial"),
        ("spaces", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            code=forwards,
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("votes", models.IntegerField(default=0)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_accepted", models.BooleanField(default=False)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "editor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Flag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("flag_type", models.TextField(max_length=300)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("votes", models.IntegerField(default=0)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                ("has_accepted_answer", models.BooleanField(default=False)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "editor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("tags", models.ManyToManyField(to="tags.tag")),
                (
                    "users_downvoted",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_forum_question_users_downvoted_+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "users_upvoted",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_forum_question_users_upvoted_+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "search_vector",
                    django.contrib.postgres.search.SearchVectorField(null=True),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TagFollow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tags.tag"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuestionFollow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="forum.question"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuestionComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("votes", models.IntegerField(default=0)),
                ("content", models.TextField(max_length=300)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "flags",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_forum_questioncomment_flags_+",
                        to="forum.flag",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="forum.question",
                    ),
                ),
                (
                    "users_upvoted",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_forum_questioncomment_users_upvoted_+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Question Comment",
                "verbose_name_plural": "Question Comments",
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="QuestionAdditionalData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("views", models.IntegerField(default=0)),
                (
                    "question",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="additional_data",
                        to="forum.question",
                    ),
                ),
            ],
            options={
                "default_related_name": "additional_data",
            },
        ),
        migrations.CreateModel(
            name="AnswerComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("votes", models.IntegerField(default=0)),
                ("content", models.TextField(max_length=300)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "answer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="forum.answer",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "flags",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_forum_answercomment_flags_+",
                        to="forum.flag",
                    ),
                ),
                (
                    "users_upvoted",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_forum_answercomment_users_upvoted_+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Answer Comment",
                "verbose_name_plural": "Answer Comments",
                "ordering": ["created_at"],
            },
        ),
        migrations.AddField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="forum.question"),
        ),
        migrations.AddField(
            model_name="answer",
            name="users_downvoted",
            field=models.ManyToManyField(
                blank=True,
                related_name="_forum_answer_users_downvoted_+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="answer",
            name="users_upvoted",
            field=models.ManyToManyField(
                blank=True,
                related_name="_forum_answer_users_upvoted_+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterOrderWithRespectTo(
            name="answer",
            order_with_respect_to="question",
        ),
        migrations.AddIndex(
            model_name="question",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["search_vector"], name="forum_quest_search__cba8ad_gin"
            ),
        ),
        migrations.AddField(
            model_name="questionfollow",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="tagfollow",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.RemoveField(
            model_name="answercomment",
            name="flags",
        ),
        migrations.RemoveField(
            model_name="questioncomment",
            name="flags",
        ),
        migrations.AddField(
            model_name="flag",
            name="content_type",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="flag",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="flag",
            name="object_id",
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="question",
            name="is_anonymous",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="QuestionBookmark",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmarks",
                        to="forum.question",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmarks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuestionInviteToAnswer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "invitee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "inviter",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invitations",
                        to="forum.question",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Question Invitations",
            },
        ),
        migrations.AddField(
            model_name="tagfollow",
            name="reputation_last_month",
            field=models.IntegerField(
                default=0,
                help_text="Reputation earned by user for tag in the past month",
            ),
        ),
        migrations.AddField(
            model_name="tagfollow",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="tagfollow",
            name="answers_by_user",
            field=models.IntegerField(default=0, help_text="Number of answers authored by user in the tag"),
        ),
        migrations.AddField(
            model_name="tagfollow",
            name="questions_by_user",
            field=models.IntegerField(default=0, help_text="Number of questions authored by user in the tag"),
        ),
        migrations.AddField(
            model_name="tagfollow",
            name="reputation",
            field=models.IntegerField(default=0, help_text="Reputation earned by user for tag"),
        ),
        migrations.CreateModel(
            name="VoteActivity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "reputation_change",
                    models.IntegerField(
                        blank=True,
                        default=None,
                        help_text="Change in reputation for target user",
                        null=True,
                    ),
                ),
                (
                    "answer",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        help_text="Answer that caused this, if relevant",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="forum.answer",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        help_text="Question caused this",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="forum.question",
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        blank=True,
                        help_text="User who voted to create this activity",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "target",
                    models.ForeignKey(
                        help_text="User affected by this activity",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reputation_votes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "seen",
                    models.DateTimeField(
                        blank=True,
                        default=None,
                        help_text="When the target user has seen this activity",
                        null=True,
                    ),
                ),
                (
                    "badge",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        help_text="Badge on this activity",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="badges.badge",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Activities",
            },
        ),
        migrations.AlterField(
            model_name="answer",
            name="editor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="editor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="IntegrationQuestion",
            fields=[
                (
                    "question",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="forum.question",
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        choices=[("slack", "Slack"), ("teams", "Microsoft Teams")],
                        max_length=10,
                    ),
                ),
                ("source_id", models.CharField(max_length=50)),
                ("link", models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name="Flag",
        ),
        migrations.CreateModel(
            name="QuestionView",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="forum.question"),
                ),
            ],
        ),
        migrations.RemoveIndex(
            model_name="question",
            name="forum_quest_search__cba8ad_gin",
        ),
        migrations.RemoveField(
            model_name="question",
            name="search_vector",
        ),
        migrations.AddField(
            model_name="questionadditionaldata",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.AddIndex(
            model_name="questionadditionaldata",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["search_vector"], name="forum_quest_search__208074_gin"
            ),
        ),
        migrations.RunPython(
            code=populate_search_vector,
            reverse_code=do_nothing,
        ),
        migrations.AlterField(
            model_name="answer",
            name="users_downvoted",
            field=models.ManyToManyField(blank=True, related_name="+", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name="answer",
            name="users_upvoted",
            field=models.ManyToManyField(blank=True, related_name="+", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name="answercomment",
            name="users_upvoted",
            field=models.ManyToManyField(blank=True, related_name="+", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name="question",
            name="users_downvoted",
            field=models.ManyToManyField(blank=True, related_name="+", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name="question",
            name="users_upvoted",
            field=models.ManyToManyField(blank=True, related_name="+", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name="questionadditionaldata",
            name="question",
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="forum.question"),
        ),
        migrations.AlterField(
            model_name="questioncomment",
            name="users_upvoted",
            field=models.ManyToManyField(blank=True, related_name="+", to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name="SearchRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("query", models.CharField(help_text="Query user did", max_length=400)),
                (
                    "results",
                    models.CharField(help_text="questionIds results", max_length=50),
                ),
                ("time", models.IntegerField(help_text="Time search has taken")),
                (
                    "author",
                    models.ForeignKey(
                        help_text="User affected by this activity",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="question",
            name="status_updated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="questionadditionaldata",
            name="link",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="questionadditionaldata",
            name="source",
            field=models.CharField(
                blank=True,
                choices=[("slack", "Slack"), ("teams", "Microsoft Teams")],
                max_length=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="questionadditionaldata",
            name="source_id",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="question",
            name="status",
            field=models.CharField(
                choices=[
                    ("a", "Open"),
                    ("t", "Triaged"),
                    ("c", "Closed"),
                    ("d", "Duplicate"),
                ],
                default="a",
                help_text="Question status",
                max_length=2,
            ),
        ),
        migrations.DeleteModel(
            name="IntegrationQuestion",
        ),
        migrations.AddField(
            model_name="question",
            name="space",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="spaces.space",
            ),
        ),
    ]
