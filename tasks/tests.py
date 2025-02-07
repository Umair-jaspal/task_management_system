from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Task

class TaskTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
            role='admin'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_task_creation(self):
        response = self.client.post(reverse('task_create'), {
            'title': 'Test Task',
            'description': 'Test Description',
            'due_date': '2023-12-31',
            'priority': 'high',
            'status': 'todo',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Task.objects.count(), 1)