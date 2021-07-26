from rest_framework import serializers

from apps.boards.models import Task
from apps.boards.serializers.comment import CommentSerializer


class TaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    comments_count = serializers.CharField(read_only=True)

    renamed_field = serializers.CharField(required=False, read_only=True, source='description')
    created_by_email = serializers.EmailField(read_only=True, source='created_by.email')
    created_by_full_name = serializers.SerializerMethodField(method_name='get_author_full_name')

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'comments', 'renamed_field', 'created_by_email', 'created_by_full_name',
                  'comments_count']
        # exclude = []

    def get_author_full_name(self, obj: Task) -> str:
        return obj.created_by.get_full_name()


class ColumnSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32)
    position = serializers.IntegerField(min_value=0)
    tasks = TaskSerializer(many=True, read_only=True)
