from rest_framework import generics, permissions

import datetime
from post import models
from . import serializers
from rest_framework.views import APIView
from rest_framework import renderers, parsers, viewsets, authentication, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from neox_project.models import CustomUser
from post.models import Post, Rating


from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='SWAGGER API')

urlpatterns = [
    url(r'^$', schema_view)
]


class PostsList(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    @staticmethod
    def get(request, format=None):
        posts = [{'id': p.id, 'title': p.title, 'content': p.content} for p in models.Post.objects.all()]
        return Response(posts)


class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class PostData(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    @staticmethod
    def get(self, request, format=None):
        posts = [{'id': p.id, 'title': p.title, 'content': p.content} for p in models.Post.objects.all()]
        return Response(posts)

    @action(detail=True, methods=['post'])
    def post(self, request, pk=None):
        user = CustomUser.objects.get(pk=request.user.id)
        try:
            p = Post.objects.get(id=request.data['post_id'])
            p.title = request.data['title']
            p.content=request.data['content']
        except (KeyError, Post.DoesNotExist):
            p = models.Post(
                title=request.data['title'],
                content=request.data['content'],
                user=user,
        )
        p.save()
        return Response({'p': str(p)})


class RatingData(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    @staticmethod
    def get(self, request, format=None):
        rating = [{'id': p.id, 'post_id': p.post_id, 'user_id': p.user_id, 'like': p.like} for p in models.Rating.objects.all()]
        return Response(rating)

    @action(detail=True, methods=['post'])
    def post(self, request, pk=None):
        user = CustomUser.objects.get(pk=request.user.id)
        try:
            r = Rating.objects.get(id=request.data['rating_id'])
            r.post = Post.objects.get(id=request.data['post_id'])
            r.user = user
            r.like = True if request.data['like'] in ['true', 'True'] else False
        except (KeyError, Rating.DoesNotExist):
            try:
                post = Post.objects.get(id=request.data['post_id'])
                r = Rating.objects.get(user=user, post=post)
                r.like = True if request.data['like'] in ['true', 'True'] else False
            except (KeyError, Rating.DoesNotExist, Post.DoesNotExist):
                r = models.Rating(
                    post=Post.objects.get(id=request.data['post_id']),
                    user=user,
                    like=True if request.data['like'] in ['true', 'True'] else False,
                )
        r.save()
        return Response({'r': str(r)})


class RatingList(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    @staticmethod
    def get(request, format=None):
        ratings = [{
            'id': r.id,
            'user_id': r.user_id,
            'post_id': r.post_id,
            'like': r.like
        } for r in models.Rating.objects.all()]
        return Response(ratings)


class DetailRating(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    queryset = models.Rating.objects.all()
    serializer_class = serializers.RatingSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class RatingCount(APIView):
    """RatingCount - class for view likes analistic"""
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = models.Rating.objects.all()

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
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = (parsers.JSONParser,)
    serializer_class = serializers.UserActivitySerializer

    @staticmethod
    def get(self, request, format=None):
        user = CustomUser.objects.get(pk=request.query_params['id'])
        res_data = {
                   'user': user.id,
                   'username': user.username,
                   'date_joined': user.date_joined,
                   'last_login': user.last_login,
               }
        return Response(res_data)
