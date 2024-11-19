# tests.py

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from .models import Project, Task, Subtask, Team, Invitation
from datetime import timedelta
from django.utils import timezone

class TeamTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user', email='user@example.com', password='userpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_team(self):
        url = reverse('team-list')  # Adjust the name according to your URL configuration
        response = self.client.post(url, {
            'name': 'Dev Team',
            'description': 'Development team',
            'lead_user': self.user.id  # Assuming 'lead_user' is required
        }, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print('Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Dev Team')


class ProjectTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user', email='user@example.com', password='userpass')
        self.team = Team.objects.create(
            name='Test Team', description='Team for testing', lead_user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_project(self):
        url = reverse('project-list')  # Adjust the name according to your URL configuration
        response = self.client.post(url, {
            'name': 'Test Project',
            'description': 'Project for testing',
            'start_date': timezone.now().date().isoformat(),
            'end_date': (timezone.now() + timedelta(days=365)).date().isoformat(),
            'status': 'Active',  # Adjust the status value if necessary
            'user': self.user.id,  # Provide 'user' as ID
            'team': self.team.id
        }, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print('Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Project')


class TaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user', email='user@example.com', password='userpass')
        self.team = Team.objects.create(
            name='Task Team', description='Team with tasks', lead_user=self.user)
        self.project = Project.objects.create(
            name='Task Project',
            description='Project with tasks',
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=365)).date(),
            status='Active',
            user=self.user,
            team=self.team
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        url = reverse('task-list')  # Adjust the name according to your URL configuration
        response = self.client.post(url, {
            'title': 'Sample Task',
            'description': 'Task for testing',
            'due_date': (timezone.now() + timedelta(days=30)).date().isoformat(),
            'status': 'Pending',  # Adjust the status value if necessary
            'priority': 1,
            'project': self.project.name,  # Provide project name as per SlugRelatedField
            'user': self.user.username,    # Provide username as per SlugRelatedField
            'assigned_to': self.user.username  # Provide username
        }, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print('Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Sample Task')


class SubtaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user', email='user@example.com', password='userpass')
        self.team = Team.objects.create(
            name='Subtask Team', description='Team with subtasks', lead_user=self.user)
        self.project = Project.objects.create(
            name='Project with Subtasks',
            description='Project testing subtasks',
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=365)).date(),
            status='Active',
            user=self.user,
            team=self.team
        )
        self.task = Task.objects.create(
            title='Main Task',
            description='Main task for subtasks',
            due_date=(timezone.now() + timedelta(days=30)).date(),
            status='In Progress',
            priority=1,
            user=self.user,
            project=self.project,
            assigned_to=self.user
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_subtask(self):
        url = reverse('subtask-list')  # Adjust the name according to your URL configuration
        response = self.client.post(url, {
            'name': 'Subtask 1',  # Use 'name' as per your model
            'description': 'Subtask for testing',
            'due_date': (timezone.now() + timedelta(days=10)).date().isoformat(),
            'status': 'Pending',  # Adjust the status value if necessary
            'task': self.task.id
        }, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print('Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Subtask 1')


class InvitationTestCase(TestCase):
    def setUp(self):
        # Create admin and normal users
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='admin123')
        self.normal_user = User.objects.create_user(
            username='user1', email='user1@example.com', password='userpass')
        self.invited_user = User.objects.create_user(
            username='invitee', email='invitee@example.com', password='inviteepass')

        # Create team and project for invitations
        self.team = Team.objects.create(
            name='Invitation Team', description='Team for invitations', lead_user=self.admin_user)
        self.project = Project.objects.create(
            name='Invite Project',
            description='Project for invitations',
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=365)).date(),
            status='Active',
            user=self.admin_user,
            team=self.team
        )

        # Clients for admin and normal user
        self.client_admin = APIClient()
        self.client_admin.force_authenticate(user=self.admin_user)

        self.client_user = APIClient()
        self.client_user.force_authenticate(user=self.normal_user)

    def test_admin_can_send_invitation(self):
        url = reverse('invitation-send-invitation')
        response = self.client_admin.post(url, {
            'user': self.invited_user.id,  # Use IDs as expected by the action
            'project': self.project.id
        }, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print('Admin Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_admin_cannot_send_invitation(self):
        url = reverse('invitation-send-invitation')
        response = self.client_user.post(url, {
            'user': self.invited_user.id,
            'project': self.project.id
        }, format='json')
        if response.status_code != status.HTTP_403_FORBIDDEN:
            print('Non-admin Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
