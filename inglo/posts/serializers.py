from rest_framework import serializers
from .models import Post, Feedback, PostLike
from sketches.serializers import SketchNestedSerializer

class PostSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'user', 'user_name' ,'title', 'content' , 'sdgs', 'likes', 'created_at']

    def get_user_name(self, obj):
        user = self.context['request'].user
        return user.name

class FeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Feedback
        fields = ['id','user', 'user_name','content', 'parent_feedback','created_at']
    
    def get_user_name(self, obj):
        user = self.context['request'].user
        return user.name

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'

class PostDetailSerializer(serializers.ModelSerializer):
    sketch = SketchNestedSerializer(read_only=True)  # 인스턴스화
    feedbacks = FeedbackSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()  # 현재 사용자가 좋아요를 눌렀는지 여부
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'user_name', 'sketch', 'title', 'content', 'sdgs', 'likes', 'created_at', 'feedbacks', 'is_liked']

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return PostLike.objects.filter(post=obj, user=user).exists()
    
    def get_user_name(self, obj):
        user = self.context['request'].user
        return user.name

    
    