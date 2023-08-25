from django.contrib.auth.models import AbstractUser

from forum import models
from forum.apps import logger
from tags.models import Tag


def create_follow_question(question: models.Question, user: AbstractUser):
    if models.QuestionFollow.objects.filter(question=question, user=user).count() > 0:
        logger.debug(f'user {user.username} trying to follow question {question.pk} which they already follow')
        return
    logger.debug(f'Adding {user.username} to question {question.id} followers')
    models.QuestionFollow.objects.create(question=question, user=user)


def delete_follow_question(question: models.Question, user: AbstractUser):
    logger.debug('Deleting follower')
    models.QuestionFollow.objects.filter(question=question, user=user).delete()


def create_follow_tag(tag: Tag, user: AbstractUser) -> models.TagFollow:
    tag_follow = models.TagFollow.objects.filter(tag=tag, user=user).first()
    if tag_follow is not None:
        logger.debug(f'user {user.username} trying to follow tag {tag.tag_word} which they already follow')
        return tag_follow
    logger.debug(f'Adding {user.username} to tag {tag.tag_word} followers')
    tag_follow = models.TagFollow.objects.create(tag=tag, user=user)
    return tag_follow


def delete_follow_tag(tag: Tag, user: AbstractUser):
    follow = models.TagFollow.objects.filter(tag=tag, user=user).first()
    if follow is None:
        logger.debug(f'user {user.username} trying to unfollow tag {tag.tag_word} which they do not follow')
        return
    logger.debug(f'Removing {user.username} from tag {tag.tag_word} followers')
    follow.delete()
