from django.urls import path
from .views import RegistreView, UserProfileView, LogoutView, PublicProfileView, SearchBySkillView, SearchFriendsView, ToggleFriendView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegistreView.as_view(), name='auth-register'),
    path('login/', TokenObtainPairView.as_view(), name='auth-token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='auth-token_refresh'),
    path('profile/', UserProfileView.as_view(), name='auth-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', PublicProfileView.as_view(), name='public-profile'),
    path('search/skills/', SearchBySkillView.as_view(), name='search-skills'),
    path('friends/search/', SearchFriendsView.as_view(), name='search-friends'),
    path('friends/toggle/<str:username>/', ToggleFriendView.as_view(), name='toggle-friend'),
]
