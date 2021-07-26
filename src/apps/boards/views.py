from django.contrib.auth.decorators import login_required
from django.db.models import Count, Prefetch
from django.http import HttpResponseRedirect
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from rest_framework import generics as rest_generic

from apps.boards.models import Board, Comment, Task
from apps.boards.serializers.comment import CommentSerializer
from apps.boards.serializers.tasks import TaskSerializer
from common.permissions import IsOwnerOrReadOnly


class CreateCommentView(generic.CreateView):
    model = Comment
    fields = ["message"]

    template_name = 'boards/create_comment_form.html'
    success_url = reverse_lazy('home:home-page')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.task = self.request.user.tasks.last()
        obj.save()
        return HttpResponseRedirect(self.get_success_url())


class DeleteComment(generic.DeleteView):
    model = Comment
    success_url = reverse_lazy('home:home-page')
    template_name = 'boards/delete_comments.html'

    def get_queryset(self):
        return super(DeleteComment, self).get_queryset().filter(created_by=self.request.user)


class BoardDetailView(generic.DetailView):
    model = Board
    context_object_name = 'board'
    template_name = 'boards/board-page.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BoardDetailView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        prefetch_tasks = Prefetch(
            'cols__tasks',
            queryset=Task.objects.select_related('col') \
                .prefetch_related('comments')
                .annotate(comments_count=Count('comments')) \
                .exclude(status=Task.STATUS_ARCHIVED)
        )
        return super(BoardDetailView, self).get_queryset() \
            .select_related('owner') \
            .prefetch_related('users', 'cols', prefetch_tasks) \
            .filter(users=self.request.user)



class CommentListCreateAPIView(rest_generic.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # def get_queryset(self):
    #     return self.queryset.filter(create_by=self.request.user)

    # def get_serializer_class(self):
    #     if self.request.version == 'v1':
    #         return "CommentSerializerV1"
    #     return CommentSerializer


class TaskListCreateAPIView(rest_generic.ListCreateAPIView):
    queryset = Task.objects.select_related('created_by').prefetch_related('comments').all()
    serializer_class = TaskSerializer
    # permission_classes = [IsOwnerOrReadOnly]
