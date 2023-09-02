from django.db import models
import datetime
from django.utils import timezone

class Question(models.Model):
    """
    this class represents a poll question in the web application.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        """
        Returns a readable string representation of the question content.
        """
        return self.question_text
    
    def was_published_recently(self):
        """
        Checks if the question was published recently.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """
    Represents a choice and it content for a poll question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        Returns a human-readable string representation of the choice.
        """
        return self.choice_text
    