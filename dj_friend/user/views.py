from multiprocessing import context
from urllib import response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from user.serializers import RegUserSerializer, AddFriendSerializer
from rest_framework.response import Response
from user.utils.friend_module import FriendsModule
from rest_framework import status, viewsets


class UserApi(viewsets.ViewSet):
    def post_registration(self, request, *_, **__):
        """Зарегестрировать юзера"""
        serializer = RegUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def get_add_friend(self, _, user_from_id, user_to_id):
        """Добавить друга"""
        response_ = FriendsModule(
            user_from_id=user_from_id, user_to_id=user_to_id
        ).send_request_friend()
        return Response({"message": str(response_[0])}, status=response_[1])

    def get_reject_friendship(self, _, user_from_id, user_to_id):
        """Отклонить дружбу"""
        response_ = FriendsModule(
            user_from_id=user_from_id, user_to_id=user_to_id
        ).reject_request_friend()
        return Response({"message": str(response_[0])}, status=response_[1])

    def get_accept_friendship(self, _, user_from_id, user_to_id):
        """Принять дружбу"""
        response_ = FriendsModule(
            user_from_id=user_from_id, user_to_id=user_to_id
        ).accept_request_friend()
        return Response({"message": str(response_[0])}, status=response_[1])

    def delete_friendship(self, _, user_from_id, user_to_id):
        """Удалить друга"""
        response_ = FriendsModule(
            user_from_id=user_from_id, user_to_id=user_to_id
        ).delete_friend()
        return Response({"message": str(response_[0])}, status=response_[1])

    def get_friend_list(self, _, user_from_id):
        """Вернет список друзей"""
        response_ = FriendsModule(user_from_id=user_from_id).get_friend_list()
        return Response({"friend_list": response_[0]}, status=response_[1])

    def get_in_out_friend_request(self, _, user_from_id):
        """Вернет список id пользователей к которому есть входящие/исходящие заявки в друзья"""
        response_ = FriendsModule(
            user_from_id=user_from_id
        ).get_lists_in_out_friend_request()
        return Response(response_[0], status=response_[1])
