from rest_framework import serializers
from .models import Post, Feedback

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # 사용자 이름 표시
    class Meta:
        model = Feedback
        fields = '__all__'
