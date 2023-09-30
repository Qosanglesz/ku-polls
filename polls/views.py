"""
Module for defining views related to polls.

This module contains Django views for handling poll-related functionality,
including voting, displaying poll details, and showing poll results.
"""
from django.http import Http404, HttpResponseRedirect
from .models import Choice, Question, Vote
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def vote(request, question_id):
    """
    Record a vote for a specific question and handle the redirection.

    Args:
        request (HttpRequest): The HTTP request object.
        question_id (int): The ID of the question to vote on.

    Returns:
        HttpResponseRedirect: Redirects to the results page after the vote is recorded.
    """
    if not request.user.is_authenticated:
        return redirect("login")
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
            messages.error(request, 'Voting for this question is not allowed as the end date has passed.')
            return HttpResponseRedirect(reverse('polls:index'))

        # Check if voting is allowed for this question
        if not question.can_vote():
            messages.error(request, "Voting for this question is not allowed at the moment.")
            return HttpResponseRedirect(reverse('polls:index'))

    this_user = request.user
    try:
        # find a vote for this user and this question
        vote = Vote.objects.get(user=this_user, choice__question=question)
        # update a choice
        vote.choice = selected_choice
        vote.save()
    except Vote.DoesNotExist:
        # No match vote = create a new Vote
        vote = Vote(user=this_user, choice=selected_choice)
        vote.save()

    # Display a success message
    messages.success(request, f"Your vote for '{question.question_text}' has been recorded successfully.")
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class IndexView(generic.ListView):
    """View for displaying the list of latest published questions."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to republished in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """View for displaying the details of a specific question."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())
    
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated, and if not, redirect to the login page.
        if not request.user.is_authenticated:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Retrieves and prepares context data for rendering a template."""
        context = super().get_context_data(**kwargs)
        user_vote = None

        if self.request.user.is_authenticated:
            try:
                # Get the user's previous vote for this question
                user_vote = Vote.objects.get(user=self.request.user, choice__question=self.object)
            except Vote.DoesNotExist:
                pass

        context['error_message'] = None
        context['user_vote'] = user_vote
        return context


class ResultsView(generic.DetailView):
    """View for displaying the results of a specific question."""

    model = Question
    template_name = 'polls/results.html'
