from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Tweet(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_update']

    @property
    def get_likes(self):
        return self.liked_by.count()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=120)
    display_picture = models.ImageField(default="/index.png")
    bio = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name', 'user']

    def __str__(self):
        return self.user.username


class FollowRelation(models.Model):
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    class Meta:
        unique_together = ['following_user', 'followed_user']

    def clean(self):
        if self.following_user == self.followed_user:
            raise ValidationError({
                'followed_user': f'following error: '
                f"Cannot follow yourself."
            })


class LikedTweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_tweets")
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="liked_by")

    class Meta:
        unique_together = ['user', 'tweet']
