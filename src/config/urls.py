"""trello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.boards.api_views import BoardViewSet
from apps.boards.views import CommentListCreateAPIView, TaskListCreateAPIView
from apps.home.views import simple_api


router = DefaultRouter()
router.register(r'boards', BoardViewSet, basename='boards')

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('boards/', include('apps.boards.urls')),
    path('users/', include('apps.users.urls')),
    path('api/users/', simple_api, name='user-endpoint'),
    path('api/boards/', include(router.urls)),
    path('api/comments/', CommentListCreateAPIView.as_view(), name='api-comments-list'),
    path('api/tasks/', TaskListCreateAPIView.as_view(), name='api-tasks-list'),
    path('', include('apps.home.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

