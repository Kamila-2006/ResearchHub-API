from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from projects.models import Project
from .models import Experiment
from rest_framework_simplejwt.tokens import RefreshToken


class ExperimentTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='password'
        )

        self.project = Project.objects.create(
            title="Test Project",
            short_description="Test Project Short Description",
            description="Test Project Description",
            start_date="2025-01-01",
            status="planning",
            visibility="public",
            group=None,
            principal_investigator=self.user
        )

        self.token = RefreshToken.for_user(self.user)
        self.auth_header = {'Authorization': f'Bearer {str(self.token.access_token)}'}

    def test_experiment_creation(self):
        url = reverse('experiment-list')
        data = {
            'title': 'Test Experiment',
            'description': 'Description of test experiment.',
            'hypothesis': 'Test hypothesis.',
            'methodology': 'Test methodology.',
            'start_date': '2025-01-01',
            'end_date': '2025-12-31',
            'status': 'planned',
            'project': self.project.id,
            'collaborators': [self.user.id]
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Experiment')

    def test_experiment_list(self):
        Experiment.objects.create(
            title='Test Experiment 2',
            description='Description for experiment 2.',
            hypothesis='Hypothesis for experiment 2.',
            methodology='Methodology for experiment 2.',
            start_date='2025-01-01',
            end_date='2025-12-31',
            status='planned',
            project=self.project
        )

        url = reverse('experiment-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_experiment_update(self):
        experiment = Experiment.objects.create(
            title='Test Experiment to Update',
            description='Experiment description.',
            hypothesis='Experiment hypothesis.',
            methodology='Experiment methodology.',
            start_date='2025-01-01',
            end_date='2025-12-31',
            status='planned',
            project=self.project
        )

        url = reverse('experiment-detail', args=[experiment.id])
        data = {
            'title': 'Updated Experiment Title',
            'description': 'Updated experiment description.',
            'hypothesis': 'Updated hypothesis.',
            'methodology': 'Updated methodology.',
            'start_date': '2025-02-01',
            'end_date': '2025-11-30',
            'status': 'ongoing',
            'project': self.project.id,
            'collaborators': [self.user.id]
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Experiment Title')

    def test_experiment_deletion(self):
        experiment = Experiment.objects.create(
            title='Test Experiment to Delete',
            description='Experiment description.',
            hypothesis='Experiment hypothesis.',
            methodology='Experiment methodology.',
            start_date='2025-01-01',
            end_date='2025-12-31',
            status='planned',
            project=self.project
        )

        url = reverse('experiment-detail', args=[experiment.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Experiment.DoesNotExist):
            Experiment.objects.get(id=experiment.id)


class ExperimentPaginationTests(APITestCase):
    def test_experiment_pagination(self):
        for i in range(15):
            Experiment.objects.create(
                title=f'Experiment {i + 1}',
                description=f'Description for experiment {i + 1}.',
                hypothesis=f'Hypothesis for experiment {i + 1}.',
                methodology=f'Methodology for experiment {i + 1}.',
                start_date='2025-01-01',
                end_date='2025-12-31',
                status='planned',
                project=Project.objects.first()
            )

        url = reverse('experiment-list') + '?page=2'
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
