from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from app.models import App, User


class UserLoginSerializer(serializers.Serializer):
    account = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(account=data['account'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Account not found.")

        if not check_password(data['password'],user.password):
            raise serializers.ValidationError("Unable to log in with provided credentials.")

        return user.account


class PasswordChangeSerializer(serializers.Serializer):
    account = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        account = data.get('account', self.context['request'].data.get('account'))

        try:
            user = User.objects.get(account=account)
        except User.DoesNotExist:
            raise serializers.ValidationError("Account not found.")

        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError("Old password is incorrect.")

        if len(data.get('new_password')) < 6:
            raise serializers.ValidationError("New password is too short.")

        if data.get('new_password') == data.get('old_password'):
            raise serializers.ValidationError("New password should be different from the old one.")

        return {'account': account, 'new_password':data.get('new_password')}

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['account', 'password']

    def create(self, validated_data):
        # 密码哈希
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = '__all__'


