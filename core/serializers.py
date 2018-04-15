from __future__ import unicode_literals
import logging
from django.conf import settings
from rest_framework import serializers

from .models import User, UserProfile
from .utils.validators import is_valid_email_domain


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id', 'job', 'job_position', 'dob'
        )
        extra_kwargs = {
            'name': {'validators': []}  # It gets really tricky here
        }


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(many=False)

    # def validate_email(self, email):
    #     """
    #     Check the email is not existed yet
    #     """
    #     if is_valid_email_domain(email):
    #         return email
    #     else:
    #         raise serializers.ValidationError(
    #             "Email không hợp lệ. Lưu ý: chỉ đăng ký bằng email Topica"
    #         )
    #         return email


    def validate_password(self, password):
        return password

    def create(self, validated_data):
        # Get list of groups that the user is belonged to
        # profile = validated_data.pop('groups')
        # Create a user with given data
        user = User.objects.create_user(**validated_data)
        user.activate()  # By default, users created by admin are activated
        # Assign user to groups

        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data.keys():
            instance.set_password(validated_data.pop('password'))
        # if 'groups' in validated_data.keys():
        #     groups = validated_data.pop('groups')
        #     # update user's group
        #     instance.groups.clear()
        #     for group in groups:
        #         instance.assign_group(group['name'])
        instance.__dict__.update(**validated_data)  # This is tricky
        instance.save()
        return instance

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'password',
            'is_active', 'profile'
        )

        read_only_fields = ('id')
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1  # For nested relations with Group
