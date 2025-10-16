from django.contrib import admin
from django.urls import path
from posts.views import PostView

urlpatterns = [
    path("posts/", PostView.as_view()),
    path('admin/', admin.site.urls),
]
