from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Follow, User
from .pagination import CustomPagination
from .serializers import FollowSerializer


class FollowUserViewSet(UserViewSet):
    pagination_class = CustomPagination

    @action(
        detail=True, permission_classes=[permissions.IsAuthenticated],
        methods=['post', 'delete']
    )
    def subscribe(self, request, id=None):
        user = request.user
        following = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if user == following:
                return Response({
                    'errors': 'Вы не можете подписываться на самого себя'
                }, status=status.HTTP_400_BAD_REQUEST)
            if Follow.objects.filter(user=user, following=following).exists():
                return Response({
                    'errors': f'Вы уже подписаны на {following.username}'
                }, status=status.HTTP_400_BAD_REQUEST)
            follow = Follow.objects.create(user=user, following=following)
            serializer = FollowSerializer(
                follow,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            follow = Follow.objects.filter(user=user, following=following)
            if follow.exists():
                follow.delete()
                return Response(
                    {f'Вы отписались от {following.username}'},
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response({
                'Вы уже отписались'
            }, status=status.HTTP_400_BAD_REQUEST)
        return None

    @action(
        detail=False, permission_classes=[permissions.IsAuthenticated],
        methods=['get']
    )
    def subscriptions(self, request):
        user = request.user
        follow = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(follow)
        serializer = FollowSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)
