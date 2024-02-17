from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'profile_img', 'country', 'language', 'liked_total', 'sketch_num', 'feedback_total','post_total','global_impact']

