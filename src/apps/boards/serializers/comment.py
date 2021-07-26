from rest_framework import serializers

from apps.boards.models import Comment


class CommentSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    created_by_id = serializers.IntegerField()
    task_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.message = validated_data.get('message', instance.message)
        instance.created_by_id = validated_data.get('created_by_id', instance.created_by_id)
        instance.task_id = validated_data.get('task_id', instance.task_id)
        instance.save()
        return instance
