from rest_framework import serializers
from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['pk', 'name', 'description', 'count', 'date_of_issue']
        read_only_fields = ['pk']

    def create(self, validated_data):
        return Book.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.count = validated_data.get('count', instance.count)
        instance.date_of_issue = validated_data.get('date_of_issue',
                                                    instance.date_of_issue)
        instance.save()
        return instance
