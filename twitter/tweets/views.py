from django.db import IntegrityError
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Tweet, UserProfile, FollowRelation, LikedTweet
from .serializers import (TweetSerializer,
                          UserProfileSerializer,
                          FollowRelationSerializer,
                          LikedTweetSerializer)
from .permissions import IsOwnerOrReadOnly


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class TweetListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, content=self.request.data["content"])


class TweetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()


class TweetLikeListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikedTweetSerializer
    queryset = LikedTweet.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(tweet=self.kwargs['pk'])

    def perform_create(self, serializer):
        current_user = self.request.user
        tweet = Tweet.objects.get(id=self.kwargs['pk'])
        try:
            # If Tweet is already liked by the current user db will throw IntegrityError
            serializer.save(user=current_user, tweet=tweet)
        except IntegrityError:
            # Delete the Like object from db
            LikedTweet.objects.get(user=current_user, tweet=tweet).delete()


class UserProfileListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class UserProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class UserFollowingListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowRelationSerializer
    queryset = FollowRelation.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(following_user=self.kwargs['pk'])

    def perform_create(self, serializer):
        current_user = self.request.user
        user_object = User.objects.get(id=self.kwargs['pk'])
        if current_user == user_object:
            raise ValidationError("Cannot follow yourself")
        try:
            # If current user is already following user db will throw IntegrityError
            serializer.save(following_user=current_user, followed_user=user_object)
        except IntegrityError:
            # Delete the follow relation from db
            FollowRelation.objects.get(following_user=current_user, followed_user=user_object).delete()


class UserFollowersListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowRelationSerializer
    queryset = FollowRelation.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(followed_user=self.kwargs['pk'])


class UserTweetListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.kwargs['pk'])
