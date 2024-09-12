from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db.models import Q
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8, max_length=16)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')

    def validate_email(self, value):
        """ we check user already exists with capital and lower case email or not."""
        if User.objects.filter(email=value.lower().strip()).exists():
            raise serializers.ValidationError("user with this email already exists.")
        return value.lower().strip()  # here we convert user's entered email into lower case

    def create(self, validated_data):
        """ if you don't override create than password not convert into HASH key. """
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'], validated_data['role'])
        return user


# for login only
class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    # token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        """  attrs is dict, so it's get value by passing key for key is not found than return None. """
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')

        if not username_or_email or not password:
            raise serializers.ValidationError({'error': 'Both Username/Email and Password are required.'})

        try:
            # get user object
            user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))  # type: ignore
        except User.DoesNotExist:
            raise serializers.ValidationError({'error': 'Invalid Username/Email.'})

        # check user profile is active or not
        if not user.is_active:
            raise serializers.ValidationError({'error': 'Your profile is disabled. please contact to Admin.'})

        # check user password credential
        if not user.check_password(password):
            raise serializers.ValidationError({'error': 'Invalid Password.'})

        attrs['user'] = user  # add user object into attributes(attrs) dict
        return attrs  # return whole user object data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8, max_length=16)
    new_password_confirmation = serializers.CharField(required=True, write_only=True, min_length=8, max_length=16)

    def validate(self, attrs):
        user = self.context['request'].user
        if attrs['new_password'] != attrs['new_password_confirmation']:
            raise serializers.ValidationError({'password_error': 'New Password & Confirm Password not match.'})

        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({'old_password': 'Invalid Old Password.'})

        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({'password_error': 'Old Password & New Password Both are Same.'})
        return attrs
