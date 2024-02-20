from rest_framework import serializers
from .models import Problem, Sketch, HMW, Crazy8Stack, Crazy8Content


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

class HMWSerializer(serializers.ModelSerializer):
    problem_content = serializers.SerializerMethodField()
    class Meta:
        model = HMW
        fields = ['id','problem','problem_content','content','created_at']
    
    def get_problem_content(self, obj):
        if obj.problem:
            return ProblemSerializer(obj.problem).data
        return None

class Crazy8ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crazy8Content
        fields = '__all__'

class Crazy8ContentForSketchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crazy8Content
        fields = ['content']

class Crazy8StackSerializer(serializers.ModelSerializer):
    contents = Crazy8ContentSerializer(many=True, read_only=True)
    hmw_content = serializers.SerializerMethodField()
    class Meta:
        model = Crazy8Stack
        fields = ['id','problem', 'hmw_content','created_at']
    
    def get_hmw_content(self, obj):
        if obj.problem:
            return HMW.objects.filter(problem=obj.problem).content

class SketchNestedSerializer(serializers.ModelSerializer):
    problem_content = serializers.SerializerMethodField()
    hmw_content = serializers.SerializerMethodField()
    crazy8_content = serializers.SerializerMethodField()

    class Meta:
        model = Sketch
        fields = ['id', 'user', 'title', 'description', 'content', 'image_url', 'created_at', 'problem_content', 'hmw_content', 'crazy8_content']

    def get_problem_content(self, obj):
        if obj.problem:
            return ProblemSerializer(obj.problem).data
        return None

    def get_hmw_content(self, obj):
        if obj.hmw:
            return HMWSerializer(obj.hmw).data
        return None

    def get_crazy8_content(self, obj):
        if obj.crazy8stack:
            crazy8_contents = Crazy8Content.objects.filter(crazy8stack=obj.crazy8stack)
            return Crazy8ContentSerializer(crazy8_contents, many=True).data
        return None

class SketchNestedSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # 사용자 정보를 문자열로 반환
    problem = serializers.CharField(source='problem.content', read_only=True)
    hmw = serializers.CharField(source='hmw.content', read_only=True)
    crazy8stack = serializers.SerializerMethodField()

    class Meta:
        model = Sketch
        fields = ['id', 'user', 'title', 'description', 'content', 'image_url', 'created_at', 'problem', 'hmw', 'crazy8stack']

    def get_crazy8stack(self, obj):
        if obj.crazy8stack:
            crazy8_contents = Crazy8Content.objects.filter(crazy8stack=obj.crazy8stack)
            return Crazy8ContentForSketchDetailSerializer(crazy8_contents, many=True).data
        return []


        
class SketchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sketch
        fields = '__all__'