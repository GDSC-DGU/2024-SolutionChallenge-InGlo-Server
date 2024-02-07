from rest_framework import serializers
from .models import Issue, IssueImage, IssueList, IssueComment

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'

class IssueImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueImage
        fields = '__all__'

class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueList
        fields = '__all__'

class IssueCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # 사용자 이름 표시
    class Meta:
        model = IssueComment
        fields = '__all__'