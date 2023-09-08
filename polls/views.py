from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice, Question
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages


def vote(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    # Check if the question is published
    if not question.is_published():
        messages.error(request, "This question is not currently published.")
        return HttpResponseRedirect(reverse('polls:index'))

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "You didn't select a choice.")
        return render(request, 'polls/detail.html', {'question': question})
    else:
        # Check if the end date has passed
        if question.end_date and timezone.now() > question.end_date:
            messages.error(request, "Voting for this question is not allowed as the end date has passed.")
            return HttpResponseRedirect(reverse('polls:index'))

        # Check if voting is allowed for this question
        if not question.can_vote():
            messages.error(request, "Voting for this question is not allowed at the moment.")
            return HttpResponseRedirect(reverse('polls:index'))

        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
