from rest_framework import serializers
from .models import Problem, Sketch, HMW, Crazy8Stack, Crazy8Content


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

class SketchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sketch
        fields = '__all__'

class HMWSerializer(serializers.ModelSerializer):
    class Meta:
        model = HMW
        fields = '__all__'

class Crazy8ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crazy8Content
        fields = '__all__'

class Crazy8StackSerializer(serializers.ModelSerializer):
    contents = Crazy8ContentSerializer(many=True, read_only=True, source='contents')

    class Meta:
        model = Crazy8Stack
        fields = '__all__'

class ProblemNestedSerializer(serializers.ModelSerializer):
    hmw = HMWSerializer(many=True, read_only=True, source='hmws')
    crazy8stack = Crazy8StackSerializer(many=True, read_only=True, source='crazy8stacks')

    class Meta:
        model = Problem
        fields = '__all__'