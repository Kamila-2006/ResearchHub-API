from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import date
from users.models import CustomUser
from projects.models import Project, Tag
from experiments.models import Experiment
from .models import Finding


class FindingViewSetTest(APITestCase):
    def setUp(self):
        self.pi = CustomUser.objects.create_user(
            email='pi@example.com', password='pass123', first_name='PI', last_name='User'
        )
        self.collaborator = CustomUser.objects.create_user(
            email='collab@example.com', password='pass123', first_name='Collab', last_name='User'
        )
        self.other_user = CustomUser.objects.create_user(
            email='other@example.com', password='pass123', first_name='Other', last_name='User'
        )
        self.project = Project.objects.create(
            title='Test Project', short_description='Short desc', description='Desc',
            start_date=date.today(), principal_investigator=self.pi
        )
        self.experiment = Experiment.objects.create(
            title='Test Experiment', description='Desc', hypothesis='Hyp', methodology='Meth',
            start_date=date.today(), end_date=date.today(), project=self.project
        )
        self.experiment.collaborators.add(self.collaborator)
        self.tag = Tag.objects.create(name="Important")
        self.finding_public = Finding.objects.create(
            title='Public Finding', description='desc', data_summary='summary', conclusion='conc',
            significance='breakthrough', visibility='public', experiment=self.experiment
        )
        self.finding_public.tags.add(self.tag)
        self.finding_private = Finding.objects.create(
            title='Private Finding', description='desc', data_summary='summary', conclusion='conc',
            significance='important', visibility='private', experiment=self.experiment
        )

    def test_list_public_findings_for_any_user(self):
        url = reverse('finding-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [item['id'] for item in response.data['results']]
        self.assertIn(self.finding_public.id, ids)

    def test_list_private_findings_for_pi(self):
        self.client.force_authenticate(user=self.pi)
        url = reverse('finding-list')
        response = self.client.get(url)
        ids = [item['id'] for item in response.data['results']]
        self.assertIn(self.finding_public.id, ids)
        self.assertIn(self.finding_private.id, ids)

    def test_list_private_findings_for_collaborator(self):
        self.client.force_authenticate(user=self.collaborator)
        url = reverse('finding-list')
        response = self.client.get(url)
        ids = [item['id'] for item in response.data['results']]
        self.assertIn(self.finding_public.id, ids)
        self.assertIn(self.finding_private.id, ids)

    def test_list_private_findings_for_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('finding-list')
        response = self.client.get(url)
        ids = [item['id'] for item in response.data['results']]
        self.assertIn(self.finding_public.id, ids)
        self.assertNotIn(self.finding_private.id, ids)

    def test_create_finding_by_pi(self):
        self.client.force_authenticate(user=self.pi)
        url = reverse('finding-list')
        data = {
            'title': 'New Finding',
            'description': 'desc',
            'data_summary': 'summary',
            'conclusion': 'conclusion',
            'significance': 'breakthrough',
            'visibility': 'public',
            'experiment': self.experiment.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_finding_by_collaborator_forbidden(self):
        self.client.force_authenticate(user=self.collaborator)
        url = reverse('finding-list')
        data = {
            'title': 'New Finding',
            'description': 'desc',
            'data_summary': 'summary',
            'conclusion': 'conclusion',
            'significance': 'important',
            'visibility': 'private',
            'experiment': self.experiment.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_finding_by_other_user_forbidden(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('finding-list')
        data = {
            'title': 'Other Finding',
            'description': 'desc',
            'data_summary': 'summary',
            'conclusion': 'conclusion',
            'significance': 'minor',
            'visibility': 'public',
            'experiment': self.experiment.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_finding_by_pi(self):
        self.client.force_authenticate(user=self.pi)
        url = reverse('finding-detail', args=[self.finding_public.id])
        data = {'title': 'Updated Finding'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_finding_by_collaborator_forbidden(self):
        self.client.force_authenticate(user=self.collaborator)
        url = reverse('finding-detail', args=[self.finding_public.id])
        data = {'title': 'Updated by Collaborator'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_finding_by_pi(self):
        self.client.force_authenticate(user=self.pi)
        url = reverse('finding-detail', args=[self.finding_public.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_finding_by_other_user_forbidden(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('finding-detail', args=[self.finding_public.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
