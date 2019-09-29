from rest_framework import serializers
from .models import UserManagers, Admin, UserAuthorize


class UserManagersSerializer(serializers.Serializer):
    uid = serializers.IntegerField(read_only=True)
    account = serializers.CharField(required=True, max_length=32)
    password = serializers.CharField(required=True, max_length=64)
    create_time = serializers.DateField(required=False)

    def validate(self, attrs):
        if UserManagers.objects.filter(account=attrs['account']).exists():
            raise serializers.ValidationError('Account is exists')

    def create(self, validated_data):
        """
        Create and return new user instance, given the validated data
        :param validated_data:
        :return:
        """
        return UserManagers.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing UserManagers instance, give the validated data
        :param instance:
        :param validated_data:
        :return:
        """
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance
