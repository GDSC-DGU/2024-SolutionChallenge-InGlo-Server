from rest_framework import serializers
from .models import Issue, IssueList, IssueComment

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'

class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueList
        fields = '__all__'

class IssueCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = IssueComment
        fields = '__all__'