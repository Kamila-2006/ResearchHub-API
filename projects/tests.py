from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from .models import Project, ProjectMember
from datetime import date

class ProjectMemberAPITest(APITestCase):
    def setUp(self):
        self.pi = CustomUser.objects.create_user(
            email='pi@example.com', password='pass123', first_name='PI', last_name='User'
        )
        self.member_user = CustomUser.objects.create_user(
            email='member@example.com', password='pass123', first_name='Member', last_name='User'
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

        self.pi_member = ProjectMember.objects.create(
            project=self.project, user=self.pi, role='principal_investigator', is_active=True
        )
        self.member = ProjectMember.objects.create(
            project=self.project, user=self.member_user, role='research_assistant', is_active=True
        )

        self.client.force_authenticate(user=self.pi)

    def test_project_member_list(self):
        url = reverse('project-member-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        if isinstance(data, dict) and 'results' in data:
            self.assertTrue(len(data['results']) >= 2)
        else:
            self.assertTrue(len(data) >= 2)

    def test_project_member_create_by_pi(self):
        url = reverse('project-member-list')
        data = {
            'project': self.project.id,
            'user': self.other_user.id,
            'role': 'collaborator',
            'is_active': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ProjectMember.objects.filter(user=self.other_user, project=self.project).exists())

    def test_project_member_create_forbidden_for_non_pi(self):
        self.client.force_authenticate(user=self.member_user)
        url = reverse('project-member-list')
        data = {
            'project': self.project.id,
            'user': self.other_user.id,
            'role': 'collaborator',
            'is_active': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_member_update_by_pi(self):
        url = reverse('project-member-detail', args=[self.member.id])
        data = {'role': 'co_investigator'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.member.refresh_from_db()
        self.assertEqual(self.member.role, 'co_investigator')

    def test_project_member_update_forbidden_for_non_pi(self):
        self.client.force_authenticate(user=self.member_user)
        url = reverse('project-member-detail', args=[self.member.id])
        data = {'role': 'co_investigator'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_member_delete_by_pi(self):
        url = reverse('project-member-detail', args=[self.member.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ProjectMember.objects.filter(id=self.member.id).exists())

    def test_project_member_delete_forbidden_for_non_pi(self):
        self.client.force_authenticate(user=self.member_user)
        url = reverse('project-member-detail', args=[self.member.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
