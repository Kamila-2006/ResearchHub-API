from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from projects.models import Project, ProjectMember
from datetime import date

class ProjectAPITest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='n_user', email='n_user@example.com', password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.project_data = {
            'title': 'AI Research',
            'short_description': 'Study on AI ethics',
            'description': 'Full details on the methodology and scope.',
            'start_date': '2025-01-01',
            'end_date': '2025-12-31',
            'status': 'planning',
            'visibility': 'public',
        }

    def test_create_project(self):
        url = reverse('project-list')
        response = self.client.post(url, self.project_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.first().title, 'AI Research')

    def test_list_projects(self):
        Project.objects.create(**self.project_data)
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_retrieve_project(self):
        project = Project.objects.create(**self.project_data)
        url = reverse('project-detail', args=[project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'AI Research')


class ProjectMemberAPITest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='user1', email='user1@example.com', password='pass123'
        )
        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(
            title='Test Project',
            short_description='Short',
            description='Full',
            start_date=date.today(),
            status='planning',
            visibility='public',
        )

    def test_add_project_member(self):
        another_user = CustomUser.objects.create_user(
            username='collab', email='collab@example.com', password='pass123'
        )

        data = {
            'project': self.project.id,
            'user': another_user.id,
            'role': 'collaborator'
        }

        url = reverse('project-member-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProjectMember.objects.count(), 1)
        self.assertEqual(ProjectMember.objects.first().user, another_user)
