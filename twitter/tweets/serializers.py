from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Tweet, UserProfile, FollowRelation, LikedTweet


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'user_id', 'last_update', 'get_likes']
        readonly = ['id', 'user_id']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user_id', 'user', 'name', 'bio', 'is_active']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        try:
            bio = validated_data.pop('bio')
        except KeyError:
            bio = ""
        profile, created = UserProfile.objects.update_or_create(user=user, name=validated_data.pop('name'), bio=bio)
        return profile


class FollowRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowRelation
        fields = ['following_user_id', 'followed_user_id']


class LikedTweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedTweet
        fields = ['user_id', 'tweet_id']
