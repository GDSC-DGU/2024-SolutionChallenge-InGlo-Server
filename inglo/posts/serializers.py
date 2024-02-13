from rest_framework import serializers
from .models import Post, Feedback, PostLike
from ..sketches.serializers import SketchNestedSerializer

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # 사용자 이름 표시
    class Meta:
        model = Feedback
        fields = '__all__'

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'

class PostDetailSerializer(serializers.ModelSerializer):
    sketch = SketchNestedSerializer(read_only=True)  # 인스턴스화
    feedbacks = FeedbackSerializer(many=True, read_only=True, source='feedbacks')
    is_liked = serializers.SerializerMethodField()  # 현재 사용자가 좋아요를 눌렀는지 여부

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return PostLike.objects.filter(post=obj, user=user).exists()

    class Meta:
        model = Post
        fields = '__all__'  # 'is_liked'는 fields에 이미 포함됩니다.
    
    