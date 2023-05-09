from django.db.models.query import QuerySet
from user.models import Friends, User
from django.db.models import Q
from rest_framework import status


class FriendsModule:
    USR_NOT_FOUND = (
        "Не найден один из пользователей, или вы пытаетесь отправить заявку себе"  #
    )
    NOW_YOU_FRIEND = "Теперь вы друзья"
    ALREADY_FRIEND = "Вы уже друзья"
    NOT_YET_ACCEPT = "Ваша заявка на дружбу еще не принята пользователем"
    SEND = "Предложение дружбы отправлено!"  #
    NOT_REQUEST_FRIEND = "Нет входящих предложений дружбы"
    NOT_REQUEST_FROM_USER = "Нет заявки в друзья от этого человека"
    EXISTS_FRIEND_REJECT = (
        "Вы являетесь друзьями, невозможно отменить принятый запрос, удалите друга."
    )
    REJECTED = "Заявка от пользователя успешно отклонена"
    DELETE_FRIEND = "Теперь вы не друзья"
    NOT_FRIENDED = "Вы не являетесь друзьями что бы удалить друга"
    STATUS_FRIENDSHIP_YES = "Вы друзья"
    STATUS_UNDER_CONSIDERATION = "Заявка в друзья еще не принята пользователем"
    STATUS_EXISTS_OUT = "От этого пользователя есть заявка в друзья"
    STATUS_NOT_REQUEST_FRIEND = "Ничего нет, ты никому не нужен"
    INCOMING = "Нет входящих заявок"
    OUTCOMING = "Нет исходящих заявок"

    def __init__(self, user_from_id, user_to_id=None) -> None:
        self.user_from_id = user_from_id
        self.user_to_id = user_to_id

    def send_request_friend(self):
        """Отправляем запрос на дружбу юзеру"""
        return self.check_users_exists()

    def check_users_exists(self) -> tuple[str, status]:
        """Проверяем существуют ли оба юзера"""
        if (
            User.objects.filter(id__in=[self.user_from_id, self.user_to_id]).count()
            == 2
        ):
            return self.check_friends(self.with_friend())
        else:
            return self.USR_NOT_FOUND, status.HTTP_400_BAD_REQUEST

    def with_friend(self) -> QuerySet:
        """Пытаемся получить заявки 2-х юзеров (отправитель и/или получатель)"""
        if self.user_to_id:
            return Friends.objects.filter(
                Q(user=self.user_from_id, user_friend=self.user_to_id)
                | Q(user=self.user_to_id, user_friend=self.user_from_id)
            )
        # return Friends.objects.filter(user=self.user_from_id, user_friend=self.user_to_id)

    def check_friends(self, friended) -> tuple[str, status]:
        """В зависимости от длинны полученного кверисета смотрим есть ли взаимные завки в друзья"""
        if len(friended) == 2:
            return self.already_friends(friended)
        elif len(friended) == 1:
            if friended[0].user.id == self.user_to_id:
                return self.auto_accept_friens(friended)
            else:
                return self.user_has_not_yet_accepted()
        else:
            return self.send_friend_request()

    def already_friends(self, friended: QuerySet) -> tuple[str, status]:
        """Если уже друзья"""
        if friended[0].friend_accept and friended[1].friend_accept:
            return self.ALREADY_FRIEND, status.HTTP_200_OK
        friended[0].friend_accept = True
        friended[1].friend_accept = True
        Friends.objects.bulk_update(friended, ["friend_accept"])
        return self.NOW_YOU_FRIEND, status.HTTP_201_CREATED

    def auto_accept_friens(self, friended: QuerySet) -> tuple[str, status]:
        """Автоматически добавляем в друзья если заявки взаимны"""
        Friends.objects.create(
            user_id=self.user_from_id,
            user_friend_id=self.user_to_id,
            friend_accept=True,
        )
        friended[0].friend_accept = True
        friended[0].save()
        return self.NOW_YOU_FRIEND, status.HTTP_201_CREATED

    def user_has_not_yet_accepted(self) -> tuple[str, status]:
        """Предложение дружбы еще не принято"""
        return self.NOT_YET_ACCEPT, status.HTTP_200_OK

    def send_friend_request(self) -> tuple[str, status]:
        """Отправка заявки в друзья"""
        Friends.objects.create(
            user_id=self.user_from_id,
            user_friend_id=self.user_to_id,
            friend_accept=False,
        )
        return self.SEND, status.HTTP_200_OK

    def accept_request_friend(self) -> tuple[str, status]:
        """Принять заявку в друзья"""
        if len(friended := self.with_friend()) >= 2:
            return self.already_friends(friended)
        elif len(friended) == 1:
            if friended[0].user_id != self.user_from_id:
                return self.auto_accept_friens(friended)
            else:
                return self.NOT_REQUEST_FROM_USER, status.HTTP_400_BAD_REQUEST
        return self.NOT_REQUEST_FRIEND, status.HTTP_400_BAD_REQUEST

    def reject_request_friend(self) -> tuple[str, status]:
        """Отклонить заявку в друзья"""
        if len(friended := self.with_friend()) >= 2:
            if friended[0].friend_accept and friended[1].friend_accept:
                return self.EXISTS_FRIEND_REJECT, status.HTTP_400_BAD_REQUEST
        if len(friended) == 1:
            if friended[0].user_id != self.user_from_id:
                friended[0].delete()
                return self.REJECTED, status.HTTP_200_OK
        return self.NOT_REQUEST_FROM_USER, status.HTTP_400_BAD_REQUEST

    def delete_friend(self) -> tuple[str, status]:
        """Удалить друга"""
        if len(friended := self.with_friend()) >= 2:
            if friended[0].friend_accept and friended[1].friend_accept:
                friended[0].delete()
                friended[1].delete()
                return self.DELETE_FRIEND, status.HTTP_204_NO_CONTENT
        return self.NOT_FRIENDED, status.HTTP_400_BAD_REQUEST

    def status_friendship(self) -> tuple[str, status]:
        """Статусы дружбы/заявок"""
        if len(friended := self.with_friend()) >= 2:
            if friended[0].friend_accept and friended[1].friend_accept:
                return self.STATUS_FRIENDSHIP_YES, status.HTTP_200_OK
        if len(friended) == 1:
            if friended[0].user_id == self.user_from_id:
                return self.STATUS_UNDER_CONSIDERATION, status.HTTP_200_OK
            elif friended[0].user_id == self.user_to_id:
                return self.STATUS_EXISTS_OUT, status.HTTP_200_OK
        return self.STATUS_NOT_REQUEST_FRIEND, status.HTTP_200_OK

    def get_friend_list(self) -> tuple[list, status]:
        if friend_list := Friends.objects.filter(
            user=self.user_from_id, friend_accept=True
        ).values_list("user_friend_id", flat=True):
            return list(friend_list), status.HTTP_200_OK
        return self.STATUS_NOT_REQUEST_FRIEND, status.HTTP_200_OK

    def get_lists_in_out_friend_request(self) -> tuple[dict, status]:
        incoming = list(
            Friends.objects.filter(
                user_friend_id=self.user_from_id, friend_accept=False
            ).values_list("user_friend_id", flat=True)
        )
        outgoing = list(
            Friends.objects.filter(
                user=self.user_from_id, friend_accept=False
            ).values_list("user_friend_id", flat=True)
        )
        return {"Входящие": incoming, "Исходящие": outgoing}, status.HTTP_200_OK
