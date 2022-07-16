from pprint import pp
from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username="adam", password="password")

    def test_can_list_posts(self):
        adam = User.objects.get(username="adam")
        Post.objects.create(owner=adam, title="title")
        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username="adam", password="password")
        response = self.client.post("/posts/", {"title": "title"})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post("/posts/", {"title": "title"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username="adam", password="password")
        brian = User.objects.create_user(username="brian", password="password")
        Post.objects.create(
            owner=adam,
            title="title",
            content="Adam's content",
        )
        Post.objects.create(
            owner=brian,
            title="title",
            content="Brian's content",
        )

    def test_user_can_retrieve_post_using_valid_id(self):
        response = self.client.get("/posts/1/")
        self.assertEqual(response.data["title"], "title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_retrieve_post_using_invalid_id(self):
        response = self.client.get("/posts/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username="adam", password="password")
        response = self.client.put("/posts/1/", {"title": "new title"})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, "new title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_other_users_post(self):
        self.client.login(username="adam", password="password")
        response = self.client.put("/posts/2/", {"title": "new title"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
