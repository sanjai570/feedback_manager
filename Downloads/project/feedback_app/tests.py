from django.test import TestCase
from django.contrib.auth.models import User
from .models import Feedback


class FeedbackModelTest(TestCase):
    def setUp(self):
        self.feedback = Feedback.objects.create(
            student_name='John Doe',
            department='IT',
            year='3',
            subject_or_faculty='Database Management',
            rating=5,
            feedback_message='Great course with excellent teaching methodology.',
            is_anonymous=False,
        )

    def test_feedback_creation(self):
        self.assertEqual(self.feedback.student_name, 'John Doe')
        self.assertEqual(self.feedback.rating, 5)

    def test_feedback_string_representation(self):
        self.assertEqual(str(self.feedback), 'John Doe - Database Management (5★)')


class FeedbackViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            password='testpass123',
            is_staff=True,
        )

    def test_feedback_form_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_admin_login_page_loads(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_requires_login(self):
        response = self.client.get('/admin/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
