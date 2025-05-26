from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import CustomUser
from .models import Group, Member


class GroupAPITest(APITestCase):

    def setUp(self):
        self.leader = CustomUser.objects.create_user(
            email='leader@example.com', password='pass123', first_name='Leader', last_name='User'
        )
        self.member_user = CustomUser.objects.create_user(
            email='member@example.com', password='pass123', first_name='Member', last_name='User'
        )
        self.other_user = CustomUser.objects.create_user(
            email='other@example.com', password='pass123', first_name='Other', last_name='User'
        )

        self.client.force_authenticate(user=self.leader)

        self.group_data = {
            'name': 'Test Group',
            'description': 'Group description',
            'institution': 'Test Institution',
            'department': 'Test Department',
            'website': 'https://example.com',
        }

        self.group = Group.objects.create(**self.group_data)
        Member.objects.create(group=self.group, user=self.leader, role='leader', is_active=True)
        Member.objects.create(group=self.group, user=self.member_user, role='member', is_active=True)

    def test_group_list_authenticated(self):
        url = reverse('group-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)

    def test_group_create_by_authenticated_user(self):
        self.client.force_authenticate(user=self.member_user)
        new_group_data = {
            'name': 'New Group',
            'description': 'New desc',
            'institution': 'Inst',
            'department': 'Dept',
            'website': 'https://newgroup.com',
        }
        url = reverse('group-list')
        response = self.client.post(url, new_group_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.filter(name='New Group').count(), 1)

    def test_group_create_forbidden_for_unauthenticated(self):
        self.client.force_authenticate(user=None)  # выход
        url = reverse('group-list')
        response = self.client.post(url, self.group_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_group_retrieve(self):
        url = reverse('group-detail', args=[self.group.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.group.name)

    def test_group_update_by_leader(self):
        url = reverse('group-detail', args=[self.group.id])
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.group.refresh_from_db()
        self.assertEqual(self.group.name, 'Updated Name')

    def test_group_update_forbidden_for_non_leader(self):
        self.client.force_authenticate(user=self.member_user)
        url = reverse('group-detail', args=[self.group.id])
        data = {'name': 'Hack Attempt'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_group_delete_by_leader(self):
        url = reverse('group-detail', args=[self.group.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Group.objects.filter(id=self.group.id).exists())

    def test_group_delete_forbidden_for_non_leader(self):
        self.client.force_authenticate(user=self.member_user)
        url = reverse('group-detail', args=[self.group.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MemberAPITest(APITestCase):

    def setUp(self):
        self.leader = CustomUser.objects.create_user(
            email='leader@example.com', password='pass123', first_name='Leader', last_name='User'
        )
        self.member_user = CustomUser.objects.create_user(
            email='member@example.com', password='pass123', first_name='Member', last_name='User'
        )
        self.other_user = CustomUser.objects.create_user(
            email='other@example.com', password='pass123', first_name='Other', last_name='User'
        )

        self.group = Group.objects.create(
            name='Test Group',
            description='Group description',
            institution='Test Institution',
            department='Test Department',
            website='https://example.com',
        )
        self.leader_member = Member.objects.create(group=self.group, user=self.leader, role='leader', is_active=True)
        self.member = Member.objects.create(group=self.group, user=self.member_user, role='member', is_active=True)

        self.client.force_authenticate(user=self.leader)

    def test_member_list(self):
        url = reverse('member-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 2)

    def test_member_create_by_leader(self):
        url = reverse('member-list')
        data = {
            'group': self.group.id,
            'user': self.other_user.id,
            'role': 'assistant',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Member.objects.filter(user=self.other_user, group=self.group).exists())

    def test_member_create_forbidden_for_non_leader(self):
        self.client.force_authenticate(user=self.member_user)  # не лидер
        url = reverse('member-list')
        data = {
            'group': self.group.id,
            'user': self.other_user.id,
            'role': 'assistant',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_member_update_by_leader(self):
        url = reverse('member-detail', args=[self.member.id])
        data = {'role': 'assistant'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.member.refresh_from_db()
        self.assertEqual(self.member.role, 'assistant')

    def test_member_update_forbidden_for_non_leader(self):
        self.client.force_authenticate(user=self.member_user)
        url = reverse('member-detail', args=[self.member.id])
        data = {'role': 'assistant'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_member_delete_by_leader(self):
        url = reverse('member-detail', args=[self.member.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Member.objects.filter(id=self.member.id).exists())

    def test_member_delete_forbidden_for_non_leader(self):
        self.client.force_authenticate(user=self.member_user)
        url = reverse('member-detail', args=[self.member.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
