from django.views import View
from django.http import JsonResponse
from .models import Post, Comment
from rest_framework import serializers

from datetime import datetime


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["date_added"] = instance.date_added.strftime("%Y-%m-%d")
        return rep


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, source="comment_set")

    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["date_posted"] = instance.date_posted.strftime("%Y-%m-%d")
        rep["comments_count"] = Comment.objects.filter(post=instance).count()
        return rep


class PostView(View):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

"""
class PostView(View):
    def get(self, request):
        posts = Post.objects.all()
        data = [post for post in posts.values()]

        for post in data:
            post["date_posted"] = datetime.strftime(post["date_posted"], "%b %d %Y")
            post["comments_count"] = Comment.objects.filter(post_id=post["id"]).count()
            post["comment"] = [comment for comment in Comment.objects.filter(post_id=post["id"]).values()]

            for comment in post["comment"]:
                comment["date_added"] = datetime.strftime(comment["date_added"], "%b %d %Y")

        return JsonResponse({"posts": data})
"""