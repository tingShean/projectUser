from rest_framework import serializers
from .models import UserManagers, Admin, UserAuthorize, PageName


class UserManagersSerializer(serializers.Serializer):
    uid = serializers.IntegerField(read_only=True)
    account = serializers.CharField(required=True, max_length=32)
    password = serializers.CharField(required=True, max_length=64)
    create_time = serializers.DateField(required=False)

    def validate(self, attrs):
        admin = UserManagers.objects.get(account=attrs['account'], password=attrs['password'])
        if not admin:
            raise serializers.ValidationError('Account is not exists or password error')

        return attrs

    def to_internal_value(self, data):
        admin = UserManagers.objects.get(account=data.get('account'), password=data.get('password'))
        if not admin:
            raise serializers.ValidationError('Account is not exists or password error')

        obj = super().to_representation(data)
        obj['uid'] = admin.uid
        obj['account'] = admin.account
        # print(obj)

        return obj


class UserManagersAddSerializer(serializers.Serializer):
    uid = serializers.IntegerField(read_only=True)
    account = serializers.CharField(required=True, max_length=32)
    password = serializers.CharField(required=True, max_length=64)
    create_time = serializers.DateField(required=False)

    def validate(self, attrs):
        if UserManagers.objects.filter(account=attrs['account']).exists():
            raise serializers.ValidationError('Account is exists')

        return attrs

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


class UserAuthorizeGetSerializer(serializers.Serializer):
    uid = serializers.IntegerField(required=True)
    page = serializers.CharField(required=False, max_length=20)
    authorize = serializers.IntegerField(required=False)

    def validate(self, attrs):
        bar_list = UserAuthorize.objects.filter(uid=attrs['uid'])
        if not bar_list.exists():
            raise serializers.ValidationError('This user not have admin authorize')

        return attrs

    def to_internal_value(self, data):
        bar_list = UserAuthorize.objects.filter(uid=data.get('uid'))
        if not bar_list.exists():
            raise serializers.ValidationError('Account is not exists or password error')

        obj = super().to_representation(data)
        obj['bar_list'] = []
        for bar in bar_list:
            obj['bar_list'].append({
                'page': bar.page,
                'authorize': bar.authorize,
            })
        # print(obj)

        return obj


class PageNameGetSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    title = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    def validate(self, attrs):
        page = PageName.objects.get(id=attrs['id'])
        if page:
            return attrs

        raise serializers.ValidationError('page not found')

    def to_internal_value(self, data):
        page = PageName.objects.get(id=data.get('id'))
        if page:
            obj = super().to_representation(data)
            obj['title'] = page.title
            obj['name'] = page.name

            return obj

        raise serializers.ValidationError('page not found')
