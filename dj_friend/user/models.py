from django.db import models

class User(models.Model):

    username = models.CharField(max_length=30, null=False, blank=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Friends(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user')
    user_friend = models.ForeignKey(User, on_delete=models.PROTECT, related_name='friends')
    friend_accept = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Друзья'
