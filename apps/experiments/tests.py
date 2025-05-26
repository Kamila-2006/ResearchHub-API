from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import date
from apps.users.models import CustomUser
from apps.projects.models import Project
from .models import Experiment


class ExperimentViewSetTest(APITestCase):
    def setUp(self):
        self.pi = CustomUser.objects.create_user(
            email='pi@example.com', password='pass123', first_name='PI', last_name='User'
        )
        self.collaborator = CustomUser.objects.create_user(
            email='collaborator@example.com', password='pass123', first_name='Collaborator', last_name='User'
        )
        self.other_user = CustomUser.objects.create_user(
            email='other@example.com', password='pass123', first_name='Other', last_name='User'
        )

        self.project = Project.objects.create(
            title='Test Project',
            short_description='Short desc',
            description='Desc',
            start_date=date.today(),
            principal_investigator=self.pi
        )

        self.experiment = Experiment.objects.create(
            title='Test Experiment',
            description='Experiment Description',
            hypothesis='Hypothesis',
            methodology='Methodology',
            start_date=date.today(),
            end_date=date.today(),
            project=self.project
        )

        self.experiment.collaborators.add(self.collaborator)

        self.client.force_authenticate(user=self.pi)

    def test_experiment_list(self):
        url = reverse('experiment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_experiment_create_by_pi(self):
        url = reverse('experiment-list')
        data = {
            'title': 'New Experiment',
            'description': 'New Experiment Description',
            'hypothesis': 'New Hypothesis',
            'methodology': 'New Methodology',
            'start_date': str(date.today()),
            'end_date': str(date.today()),
            'project': self.project.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Experiment.objects.filter(title='New Experiment').exists())

    def test_experiment_create_forbidden_for_non_pi(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('experiment-list')
        data = {
            'title': 'New Experiment',
            'description': 'New Experiment Description',
            'hypothesis': 'New Hypothesis',
            'methodology': 'New Methodology',
            'start_date': str(date.today()),
            'end_date': str(date.today()),
            'project': self.project.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_experiment_update_by_pi(self):
        url = reverse('experiment-detail', args=[self.experiment.id])
        data = {'title': 'Updated Experiment'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experiment.refresh_from_db()
        self.assertEqual(self.experiment.title, 'Updated Experiment')

    def test_experiment_update_forbidden_for_non_pi(self):
        self.client.force_authenticate(user=self.collaborator)
        url = reverse('experiment-detail', args=[self.experiment.id])
        data = {'title': 'Updated Experiment by Collaborator'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_experiment_delete_by_pi(self):
        url = reverse('experiment-detail', args=[self.experiment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Experiment.objects.filter(id=self.experiment.id).exists())

    def test_experiment_delete_forbidden_for_non_pi(self):
        self.client.force_authenticate(user=self.collaborator)
        url = reverse('experiment-detail', args=[self.experiment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
