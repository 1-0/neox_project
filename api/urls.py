from django.urls import path, include
from . import views
from rest_auth.registration import urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('posts/', views.PostsList.as_view(), name="posts_list"),
    path('post/<int:pk>/', views.DetailPost.as_view(), name="post"),
    path('ratings/', views.RatingList.as_view(), name="rating_list"),
    path('rating/<int:pk>/', views.DetailRating.as_view(), name="rating"),
    path('analitics/', views.RatingCount.as_view(), name="rating_count"),
    path('analitics/<int:pk>/', views.DetailRating.as_view(), name="rating_detail"),
    path('rest-auth/', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
]

# api/ registration/ ^$ [name='rest_register']
# api/ registration/ ^verify-email/$ [name='rest_verify_email']
# api/ registration/ ^account-confirm-email/(?P<key>[-:\w]+)/$ [name='account_confirm_email']

# api/ rest-auth/ ^password/reset/$ [name='rest_password_reset']
# api/ rest-auth/ ^password/reset/confirm/$ [name='rest_password_reset_confirm']
# api/ rest-auth/ ^login/$ [name='rest_login']
# api/ rest-auth/ ^logout/$ [name='rest_logout']
# api/ rest-auth/ ^user/$ [name='rest_user_details']
# api/ rest-auth/ ^password/change/$ [name='rest_password_change']


