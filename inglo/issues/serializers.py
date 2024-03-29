from rest_framework import serializers
from .models import Issue, IssueList, IssueComment, IssueLike
from accounts.serializers import UserSemiSerializer

class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueList
        fields = '__all__'

class IssueCommentSerializer(serializers.ModelSerializer):
    user = UserSemiSerializer(read_only=True)

    class Meta:
        model = IssueComment
        fields = ['id', 'user' ,'content', 'parent_comment', 'created_at']

class IssueLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueLike
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    comments = IssueCommentSerializer(many=True, read_only=True)
    user_has_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Issue
        fields = '__all__'

    def get_user_has_liked(self, obj):
        user = self.context.get('request').user
        return IssueLike.objects.filter(issue=obj, user=user).exists()