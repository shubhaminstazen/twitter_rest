from django.contrib import admin

from .models import Tweet, UserProfile, FollowRelation, LikedTweet


class PostTweets(admin.ModelAdmin):
    list_display = ["id", "content"]

    class Meta:
        model = Tweet


class ShowFollow(admin.ModelAdmin):
    list_display = ["following_user", "followed_user"]

    class Meta:
        model = FollowRelation


class ShowLikes(admin.ModelAdmin):
    list_display = ["user", "tweet"]

    class Meta:
        model = LikedTweet


# Register your models here.
admin.site.register(FollowRelation, ShowFollow)
admin.site.register(LikedTweet, ShowLikes)
admin.site.register(Tweet, PostTweets)
admin.site.register(UserProfile)
