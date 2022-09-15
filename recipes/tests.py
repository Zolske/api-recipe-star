from django.contrib.auth.models import User
from .models import Recipe
from rest_framework import status
from rest_framework.test import APITestCase


class RecipeListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='tester', password='pass')

    def test_can_list_recipe(self):
        tester = User.objects.get(username='tester')
        Recipe.objects.create(owner=tester, title='a title')
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_recipe(self):
        self.client.login(username='tester', password='pass')
        response = self.client.post('/recipes/', {'title': 'a title'})
        count = Recipe.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_recipe(self):
        response = self.client.post('/recipes/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RecipeDetailViewTests(APITestCase):
    def setUp(self):
        tester_1 = User.objects.create_user(username='tester_1', password='pass')
        tester_2 = User.objects.create_user(username='tester_2', password='pass')
        Recipe.objects.create(
            owner=tester_1, title='a title', content='tester_1s content'
        )
        Recipe.objects.create(
            owner=tester_2, title='another title', content='tester_2s content'
        )

    def test_can_retrieve_recipe_using_valid_id(self):
        response = self.client.get('/recipes/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_recipe_using_invalid_id(self):
        response = self.client.get('/recipes/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_recipe(self):
        self.client.login(username='tester_1', password='pass')
        response = self.client.put('/recipes/1/', {'title': 'a new title'})
        recipe = Recipe.objects.filter(pk=1).first()
        self.assertEqual(recipe.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_recipe(self):
        self.client.login(username='tester_1', password='pass')
        response = self.client.put('/recipes/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)