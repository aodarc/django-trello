from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
# Create your views here.
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.boards.models import Task


def home_page(request):
    return HttpResponse("<h1>Hello</h1>")


@login_required
def simple_api(request):
    data = serializers.serialize('json', [request.user])
    return HttpResponse(data)


class HomePage(TemplateView):
    template_name = 'pages/home.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HomePage, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['now'] = timezone.now()
        context['user'] = self.request.user
        context['user_json'] = serializers.serialize('json', [self.request.user])
        context['tasks'] = Task.objects.all().order_by('-id')
        return context
