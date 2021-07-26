from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.boards.models import Board
from apps.boards.serializers.tasks import ColumnSerializer, TaskSerializer


class BoardSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=36)
    owner_name = serializers.SerializerMethodField(method_name='get_owner_full_name')
    owner_full_name = serializers.CharField(read_only=True)
    cols = ColumnSerializer(many=True)


    def get_owner_full_name(self, obj: Board) -> str:
        return obj.owner.get_full_name()

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Board.objects.all(),
                fields=['name', 'owner']
            )
        ]

    def validate_cols(self, value):

        return value

    # bla = Board.objects.filter(is_active=True)
    # bla = Board.objects.active()
