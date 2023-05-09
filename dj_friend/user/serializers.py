from rest_framework import serializers
from user.models import Friends, User
from django.db.models import Q

class RegUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'id']
        read_only_fields = ['id']

class AddFriendSerializer(serializers.Serializer):

    def validate(self, data):
        if isinstance(data.get('user_from_id', None), int) and isinstance(data.get('user_to_id', None), int):
            return data
        raise serializers.ValidationError('id пользователей должен быть целым числом (int)')
