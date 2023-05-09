from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import User, Friends


class FriendListDeleteTest(APITestCase):
    def setUp(self):
        user_1 = User.objects.create(username="user")
        user_2 = User.objects.create(username="user")
        Friends.objects.create(user_id=user_1.id, user_friend_id=user_2.id)
        self.user_1 = user_1.id
        self.user_2 = user_2.id

    def test_registration_user(self):
        response_ = self.client.post(
            reverse("registration_user"), data={"username": "vasya"}
        )
        assert response_.status_code == 200

    def test_add_friend_user(self):
        response_ = self.client.get(
            reverse("add_friend", args=(self.user_1, self.user_2))
        )
        assert response_.status_code == 200

    def test_accept_friend_user(self):
        response_ = self.client.get(
            reverse("accept_friend", args=(self.user_2, self.user_1))
        )
        assert response_.status_code == 201
