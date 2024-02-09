from rest_framework import serializers
from .models import Issue, IssueList, IssueComment

class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueList
        fields = '__all__'

class IssueCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = IssueComment
        fields = '__all__'
        read_only_fields = ['id', 'user', 'issue', 'parent_comment', 'created_at']

class IssueSerializer(serializers.ModelSerializer):
    comments = IssueCommentSerializer(many=True, read_only=True, source='issuecomment_set')
    
    class Meta:
        model = Issue
        fields = '__all__'