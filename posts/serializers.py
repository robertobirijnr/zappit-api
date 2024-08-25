from rest_framework import serializers
from .models import Post,Vote

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    votes = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','title','url','user','created','votes']

    def get_votes(self,post):
        return Vote.objects.filter(post=post).count()

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']        