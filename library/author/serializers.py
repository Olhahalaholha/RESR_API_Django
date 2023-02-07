import logging

from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=20)
    surname = serializers.CharField(max_length=20)
    patronymic = serializers.CharField(max_length=20, allow_blank=True)

    class Meta:
        model = Author
        fields = '__all__'

    def create(self, validated_data):
        logging.warning(validated_data)
        name = validated_data.get('name')
        surname = validated_data.get('surname')
        patronymic = validated_data.get('patronymic')
        return Author.create(name, surname, patronymic)

    def partial_update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.surname = validated_data.get("surname", instance.surname)
        instance.patronymic = validated_data.get("patronymic", instance.patronymic)
        instance.save()
        return instance


