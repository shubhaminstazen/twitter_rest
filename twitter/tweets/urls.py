from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'tweets'

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('tweets/', views.TweetListCreateView.as_view(), name='tweet_list_create'),
    path('tweets/<int:pk>/', views.TweetRetrieveUpdateDestroyView.as_view(), name='tweet_detail'),
    path('tweets/<int:pk>/like/', views.TweetLikeListCreateView.as_view(), name='tweet_like_detail'),
    path('users/', views.UserProfileListCreateView.as_view(), name='users_list_create'),
    path('users/<int:pk>/', views.UserProfileRetrieveUpdateDestroyView.as_view(), name='users_detail'),
    path('users/<int:pk>/following/', views.UserFollowingListCreateView.as_view(), name='user_following'),
    path('users/<int:pk>/followers/', views.UserFollowersListView.as_view(), name='user_followers'),
    path('users/<int:pk>/tweets/', views.UserTweetListView.as_view(), name='user_tweets'),
]
