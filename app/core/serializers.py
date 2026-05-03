from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
    )

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validate_password(password)
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            validate_password(password, user)
            user.set_password(password)
            user.save()

        return user
