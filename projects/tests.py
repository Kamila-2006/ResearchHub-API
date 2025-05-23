from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from groups.models import Group
from .models import Project, ProjectMember
from rest_framework_simplejwt.tokens import RefreshToken


class ProjectTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='password'
        )
        self.group = Group.objects.create(name="Research Group")
        self.project = Project.objects.create(
            title="Test Project",
            short_description="A short description",
            description="A long description",
            start_date="2025-01-01",
            status="planning",
            visibility="public",
            group=self.group,
            principal_investigator=self.user
        )
        self.token = RefreshToken.for_user(self.user)
        self.auth_header = {'Authorization': f'Bearer {str(self.token.access_token)}'}

    def test_project_creation(self):
        url = reverse('project-list')
        data = {
            'title': 'New Project',
            'short_description': 'Short description for new project',
            'description': 'Long description for new project',
            'start_date': '2025-02-01',
            'status': 'in_progress',
            'visibility': 'private',
            'group': self.group.id,
            'principal_investigator': self.user.id
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Project')

    def test_project_list(self):
        url = reverse('project-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_project_member_creation(self):
        url = reverse('project-member-list')
        member_data = {
            'user': self.user.id,
            'project': self.project.id,
            'role': 'principal_investigator',
        }
        response = self.client.post(url, member_data, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['role'], 'principal_investigator')

    def test_project_member_list(self):
        ProjectMember.objects.create(user=self.user, project=self.project, role='principal_investigator')
        url = reverse('project-member-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_project_update(self):
        url = reverse('project-detail', args=[self.project.id])
        data = {
            'title': 'Updated Project Title',
            'short_description': 'Updated short description',
            'description': 'Updated long description',
            'start_date': '2025-01-01',
            'status': 'completed',
            'visibility': 'private',
            'group': self.group.id,
            'principal_investigator': self.user.id
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Project Title')

    def test_project_member_update(self):
        member = ProjectMember.objects.create(user=self.user, project=self.project, role='research_assistant')
        url = reverse('project-member-detail', args=[member.id])
        data = {
            'role': 'co_investigator',
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'co_investigator')

    def test_project_deletion(self):
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Project.DoesNotExist):
            Project.objects.get(id=self.project.id)

    def test_project_member_deletion(self):
        member = ProjectMember.objects.create(user=self.user, project=self.project, role='research_assistant')
        url = reverse('project-member-detail', args=[member.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ProjectMember.DoesNotExist):
            ProjectMember.objects.get(id=member.id)

        class ProjectMemberTests(APITestCase):
            pass
