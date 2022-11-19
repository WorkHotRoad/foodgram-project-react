from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response

from .models import Follow, User
from .pagination import LimitPageNumberPagination
from .serializers import FollowSerializer, ShowFollowsSerializer


class FollowUserViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination

    @action(
        detail=True, permission_classes=[permissions.IsAuthenticated],
        methods=['post', 'delete']
    )
    def subscribe(self, request, id=None):
        following = get_object_or_404(User, id=id)
        serializer = FollowSerializer(
            data={'user': request.user.id, 'following': id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'POST':
            serializer.save(user=request.user)
            serializer = ShowFollowsSerializer(
                following, context={'request': self.request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        follow = get_object_or_404(
            Follow, user=request.user, following__id=id
        )
        follow.delete()
        return Response(
            f'ВЫ отписались от {follow.following}',
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=False, permission_classes=[permissions.IsAuthenticated],
        methods=['get']
    )
    def subscriptions(self, request):
        user = User.objects.filter(following__user=request.user)
        pages = self.paginate_queryset(user)
        serializer = ShowFollowsSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
