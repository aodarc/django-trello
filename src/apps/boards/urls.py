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
from django.urls import path

from apps.boards.views import BoardDetailView, CreateCommentView, DeleteComment

app_name = 'home'

urlpatterns = [
    # path('home/', home_page, name='home-page'),
    path('<int:pk>', BoardDetailView.as_view(), name='board-detail'),
    path('comments/create', CreateCommentView.as_view(), name='comments-create'),
    path('comments/<int:pk>/delete', DeleteComment.as_view(), name='comments-delete'),
]
