from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from forum.apps import logger
from forum.views import utils


@login_required
def view_delete_question(request, pk: int):
    question = utils.get_model("question", pk)
    user = request.user
    if question is None:
        logger.warning(
            f"user {user.username} tried to delete question {pk} which does not exist"
        )
        return redirect("forum:list")

    if question.author != user and not user.can_delete_question:
        logger.warning(
            f"user {user.username} tried to delete question {pk} "
            f"which does they do not have permission to delete"
        )
        return redirect("forum:thread", pk=pk)
    if request.method == "POST":
        utils.delete_question(question)
        messages.success(request, "Question deleted")
        return redirect("forum:list")
    # Get request
    return render(
        request,
        "main/deletequestion.html",
        {
            "title": question.title,
            "content": question.content,
            "pk": pk,
        },
    )
