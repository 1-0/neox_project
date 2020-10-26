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
    path('add_post/', views.PostViewSet.as_view(), name="add_post"),
    path('post/<int:pk>/', views.DetailPost.as_view(), name="post"),
    path('ratings/', views.RatingList.as_view(), name="rating_list"),
    path('rating/<int:pk>/', views.DetailRating.as_view(), name="rating"),
    path('analitics/', views.RatingCount.as_view(), name="rating_count"),
    path('analitics/<int:pk>/', views.DetailRating.as_view(), name="rating_detail"),
    path('rest-auth/', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    path('', views.schema_view, name="schema_view"),
]


