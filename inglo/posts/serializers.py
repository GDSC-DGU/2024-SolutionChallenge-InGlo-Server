from rest_framework import serializers
from .models import Post, Feedback, PostLike
from accounts.serializers import UserSemiSerializer
from sketches.serializers import SketchNestedSerializer
from logging import getLogger

logger = getLogger('django')

class PostSerializer(serializers.ModelSerializer):
    user = UserSemiSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'user','title', 'content' , 'sdgs', 'likes', 'created_at']

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSemiSerializer(read_only=True)
    class Meta:
        model = Feedback
        fields = ['id','user','content', 'parent_feedback','created_at'] 

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'

class PostDetailSerializer(serializers.ModelSerializer):
    sketch = SketchNestedSerializer(read_only=True)  # 인스턴스화
    feedbacks = FeedbackSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()  # 현재 사용자가 좋아요를 눌렀는지 여부
    user = UserSemiSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'sketch', 'title', 'content', 'sdgs', 'likes', 'created_at', 'feedbacks', 'is_liked']

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return PostLike.objects.filter(post=obj, user=user).exists()

    
    