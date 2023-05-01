from .models import Book
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', "best_seller", "num_pages"]
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        book = Book.objects.create(**validated_data)
        return book
