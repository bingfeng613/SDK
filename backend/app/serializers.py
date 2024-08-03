from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from app.models import App, User


class UserLoginSerializer(serializers.Serializer):
    account = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        print(data.get('account'))
        user = User.objects.filter(account=data.get('account')).first()
        if user and user.password == data.get('password'):
            return {'user': user}
        raise serializers.ValidationError('Unable to log in with provided credentials.')

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Old password is incorrect'})

        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'account', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = '__all__'


