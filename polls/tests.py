import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice
from django.contrib.auth.models import User


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_now(self):
        """
        is_published() should return True for questions with currently time.
        """
        current_time = timezone.now()
        question = Question(pub_date=current_time)
        self.assertTrue(question.is_published())

    def test_is_published_with_past(self):
        """
        is_published() should return True for questions with a pub date in the past.
        """
        past_pub_date = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=past_pub_date)
        self.assertTrue(question.is_published())

    def test_cannot_vote_after_end_date(self):
        """
        Cannot vote if the end_date is in the past.
        """
        past_end_date = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=timezone.now(), end_date=past_end_date)
        self.assertFalse(question.can_vote())

    def test_can_vote_null_end_date(self):
        """
        Can vote if end_date is Null.
        """
        question = Question(pub_date=timezone.now(), end_date=None)
        self.assertTrue(question.can_vote())

    def test_can_vote_with_end_date_in_future(self):
        """
        can_vote() should return True for questions with an end_date in the future.
        """
        future_end_date = timezone.now() + timezone.timedelta(days=1)
        question = Question(pub_date=timezone.now(), end_date=future_end_date)
        self.assertTrue(question.can_vote())

    def test_cannot_vote_before_pub_date(self):
        """
        Cannot vote if the current time is before the pub_date.
        """
        future_pub_date = timezone.now() + datetime.timedelta(days=1)
        question = Question(pub_date=future_pub_date, end_date=future_pub_date + datetime.timedelta(days=1))
        self.assertFalse(question.can_vote())


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

    class QuestionDetailViewTests(TestCase):
        def test_future_question(self):
            """
            The detail view of a question with a pub_date in the future
            returns a 404 not found.
            """
            future_question = create_question(question_text='Future question.', days=5)
            url = reverse('polls:detail', args=(future_question.id,))
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)

        def test_past_question(self):
            """
            The detail view of a question with a pub_date in the past
            displays the question's text.
            """
            past_question = create_question(question_text='Past Question.', days=-5)
            url = reverse('polls:detail', args=(past_question.id,))
            response = self.client.get(url)
            self.assertContains(response, past_question.question_text)


class AuthenticationTestCase(TestCase):
    """
    Test case for user authentication.
    """

    def setUp(self):
        """
        Set up test data and create a user.
        """
        self.username = 'Vader'
        self.password = '@Iamyourfater'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login(self):
        """
        Test user login functionality.
        """
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        """
        Test user logout functionality.
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class VoteAuthenticationTestCase(TestCase):
    """
    Test case for user authentication when voting in polls.
    """

    def setUp(self):
        """
        Set up test data including a user, a question, and choices.
        """
        self.username = 'Vader'
        self.password = '@Iamyourfater'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.question = Question.objects.create(question_text='Test Question')
        self.choice1 = Choice.objects.create(question=self.question, choice_text='Choice 1')
        self.choice2 = Choice.objects.create(question=self.question, choice_text='Choice 2')

    def test_vote_authentication(self):
        """
        Test user authentication when voting in a poll.
        """
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice1.id})
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice1.id})
        self.assertIn(response.status_code, [200, 302])

    def test_change_vote_authentication(self):
        """
        Test changing a vote with user authentication.
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice1.id})
        self.assertIn(response.status_code, [200, 302])
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice2.id})
        self.assertIn(response.status_code, [200, 302])

    def test_change_vote_unauthenticated(self):
        """
        Test changing a vote without user authentication.
        """
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice1.id})
        self.assertEqual(response.status_code, 302)

    def test_one_vote_per_poll(self):
        """
        Test allowing only one vote per poll for a user.
        """
        self.client.login(username=self.username, password=self.password)
        response1 = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice1.id})
        self.assertIn(response1.status_code, [200, 302])
        response2 = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice1.id})
        self.assertEqual(response2.status_code, 302)
