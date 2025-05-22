from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from .models import Group, Member
from rest_framework_simplejwt.tokens import RefreshToken

class GroupTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )

        self.group = Group.objects.create(
            name='Test Group',
            description='Test Group Description',
            institution='Test Institution',
            department='Test Department',
            website='http://testgroup.com'
        )

        self.token = RefreshToken.for_user(self.user)
        self.auth_header = {'Authorization': f'Bearer {str(self.token.access_token)}'}

    def test_group_creation(self):
        url = reverse('group-list')
        data = {
            'name': 'New Group',
            'description': 'A new test group.',
            'institution': 'Test Institution',
            'department': 'Test Department',
            'website': 'http://newgroup.com',
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Group')

    def test_group_list(self):
        Group.objects.create(
            name='Another Test Group',
            description='Another test group description.',
            institution='Test Institution',
            department='Test Department',
            website='http://anothergroup.com'
        )

        url = reverse('group-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_group_update(self):
        url = reverse('group-detail', args=[self.group.id])
        data = {
            'name': 'Updated Test Group',
            'description': 'Updated description.',
            'institution': 'Updated Institution',
            'department': 'Updated Department',
            'website': 'http://updatedgroup.com',
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Test Group')

    def test_group_deletion(self):
        url = reverse('group-detail', args=[self.group.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Group.DoesNotExist):
            Group.objects.get(id=self.group.id)


class MemberTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.group = Group.objects.create(
            name='Test Group',
            description='Test Group Description',
            institution='Test Institution',
            department='Test Department',
            website='http://testgroup.com'
        )

        self.member = Member.objects.create(
            group=self.group,
            user=self.user,
            role='leader'
        )

        self.token = RefreshToken.for_user(self.user)
        self.auth_header = {'Authorization': f'Bearer {str(self.token.access_token)}'}

    def test_member_creation(self):
        url = reverse('member-list')
        data = {
            'group': self.group.id,
            'user': self.user.id,
            'role': 'assistant',
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['role'], 'assistant')

    def test_member_list(self):
        url = reverse('member-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_member_update(self):
        url = reverse('member-detail', args=[self.member.id])
        data = {
            'role': 'member',
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'member')

    def test_member_deletion(self):
        url = reverse('member-detail', args=[self.member.id])
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth_header['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Member.DoesNotExist):
            Member.objects.get(id=self.member.id)

