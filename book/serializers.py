from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Books

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('title', 'author')

class TokenSerializer(serializers.Serializer):
        
    token = serializers.CharField(max_length=255)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
