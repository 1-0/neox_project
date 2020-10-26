from rest_framework import generics, permissions

import datetime
from post import models
from . import serializers
from rest_framework.views import APIView
from rest_framework import renderers, parsers
from rest_framework.response import Response
from rest_framework import authentication, permissions
from neox_project.models import CustomUser


class PostsList(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, ]
    # renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, format=None):
        posts = [{'id': p.id, 'title': p.title, 'content': p.content} for p in models.Post.objects.all()]
        return Response(posts)


class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class RatingList(generics.ListCreateAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    queryset = models.Rating.objects.all()
    serializer_class = serializers.RatingSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class DetailRating(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    queryset = models.Rating.objects.all()
    serializer_class = serializers.RatingSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class RatingCount(APIView):
    """RatingCount - class for view likes analistic"""
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = models.Rating.objects.all()
    # renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, format=None):
        if 'date' in request.query_params:
            d = datetime.date.fromisoformat(request.query_params['date'])
            self.query_set = models.Rating.objects.filter(pub_date__contains=d, like=True)
        elif 'date_from' in request.query_params or 'date_to' in request.query_params:
            if 'like' in request.query_params:
                like = (request.query_params['like'] in ['True', 'true'])
            else:
                like = True
            d0 = datetime.date.fromisoformat(request.query_params['date_from']) \
                if ('date_from' in request.query_params) \
                else datetime.date(1970, 1, 1)
            d1 = datetime.date.fromisoformat(request.query_params['date_to']) \
                if ('date_to' in request.query_params) \
                else datetime.date.today()
            self.query_set = models.Rating.objects.filter(
                pub_date__gte=d0
            ).filter(
                pub_date__lte=d1
            ).filter(
                like=like
            )
        else:
            query_set = models.Rating.objects.all()
        rating_count = query_set.count()
        return Response({'rating_count': rating_count})


class UserActivity(APIView):
    """UserActivity - class for view user activity"""
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = (parsers.JSONParser,)
    serializer_class = serializers.UserActivitySerializer
    # renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, format=None):
        user = CustomUser.objects.get(pk=request.query_params['id'])
        res_data = {
                   'user': user.id,
                   'username': user.username,
                   'date_joined': user.date_joined,
                   'last_login': user.last_login,
               }
        return Response(res_data)
