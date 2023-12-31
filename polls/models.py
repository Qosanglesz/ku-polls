"""This module defines a Django model for representing Date data andprovides more information about the models."""
from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """this class represents a poll question in the web application."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    end_date = models.DateTimeField("date ended", null=True)

    def __str__(self):
        """Returns a readable string representation of the question content."""
        return self.question_text

    def was_published_recently(self):
        """Checks if the question was published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Checks if the question is currently published."""
        now = timezone.localdate()  # Use local date/time
        return now >= self.pub_date.date()

    def can_vote(self):
        """Checks if voting is allowed for this question."""
        now = timezone.localtime()  # Use local date/time
        return self.pub_date <= now <= (self.end_date or timezone.now())


class Choice(models.Model):
    """Represents a choice and it content for a poll question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        """Returns a human-readable string representation of the choice."""
        return self.choice_text

    @property
    def votes(self):
        """Return the number of votes for this choice."""
        count = Vote.objects.filter(choice=self).count()
        return count


class Vote(models.Model):
    """Records a Vote of a Choice by a User"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
