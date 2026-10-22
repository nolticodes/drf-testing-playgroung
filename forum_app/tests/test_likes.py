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
        

        # self.token = Token.objects.create(user=self.user)
        # self.client = APIClient()
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_like(self):
        url = reverse('like-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_like(self):
        url = reverse('like-detail', kwargs={'pk': self.like.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
