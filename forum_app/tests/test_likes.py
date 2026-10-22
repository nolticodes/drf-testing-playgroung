from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from forum_app.models import Like, Question


class LikeTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.question = Question.objects.create(
            title='Test Question', content='Test Content', author=self.user, category='frontend')
        self.like = Like.objects.create(
            user=self.user, question=self.question)
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpassword'
        )
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpassword',
            is_staff=True
        )

        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.other_token = Token.objects.create(user=self.other_user)

        self.admin_token = Token.objects.create(user=self.admin)

    def test_get_like(self):
        url = reverse('like-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_like(self):
        url = reverse('like-detail', kwargs={'pk': self.like.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_like_not_found(self):
        like_id = self.like.id
        self.like.delete()
        url = reverse('like-detail', kwargs={'pk': like_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_like_succes(self):
        self.like.delete()
        url = reverse('like-list')
        data = {
            'user': self.user.id,
            'question': self.question.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_like_missing_data(self):
        self.like.delete()
        url = reverse('like-list')
        data = {
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_post_owner(self):
        url = reverse('like-detail', kwargs={'pk': self.like.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_not_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.other_token.key
        )
        url = reverse('like-detail', kwargs={'pk': self.like.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.admin_token.key
        )
        url = reverse('like-detail', kwargs={'pk': self.like.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
