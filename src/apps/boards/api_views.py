from django.db.models import Count, Prefetch, Value
from django.db.models.functions import Concat
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.boards.models import Board, Col, Task
from apps.boards.serializers.board import BoardSerializer


class BoardViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Board.objects.active()
    serializer_class = BoardSerializer

    def get_queryset(self):
        prefetch_tasks = Prefetch(
            'cols__tasks',
            queryset=Task.objects.select_related('col', 'created_by') \
                .prefetch_related('comments')
                .annotate(comments_count=Count('comments')) \
                .exclude(status=Task.STATUS_ARCHIVED)
        )
        prefetch_cols = Prefetch(
            'cols',
            queryset=Col.objects.active().order_by('position')
        )
        return super().get_queryset() \
            .select_related('owner') \
            .prefetch_related('users', prefetch_cols, prefetch_tasks) \
            .annotate(owner_full_name=Concat('owner__first_name', Value(' '), 'owner__last_name'))

    @action(detail=True, methods=['put', 'patch'])
    def change_task_ordering(self, request, pk=None):
        board = self.get_object()
        data = request.data
        # TODO
        if 'columns' in data:
            pass
        columns_dict = board.cols.in_bulk([item['id'] for item in data['columns']])

        columns_set = set(columns_dict.keys())

        for col in (col for col in data['columns'] if col['id'] in columns_set):
            columns_dict[col['id']].position = col['position']

        Col.objects.bulk_update(list(columns_dict.value()), ['position'])

        return Response({})


