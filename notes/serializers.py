from rest_framework.serializers import ModelSerializer
from .models import Notes, Labels
from rest_framework import serializers


class NotesSerializer(ModelSerializer):
    class Meta:
        model = Notes

        fields = [
            'title', 'description', 'id', 'owner_id','collaborator','label'
        ]


class LabelsSerializer(ModelSerializer):
    class Meta:
        model = Labels
        fields = ['name', 'owner', 'id']
        extra_kwargs = {'owner': {'read_only': True}}


class CollaboratorSerializer(ModelSerializer):
    collaborator = serializers.EmailField()

    class Meta:
        model = Notes
        fields = ['collaborator']


class AddLabelsToNoteSerializer(serializers.ModelSerializer):
    label = serializers.CharField()

    class Meta:
        model = Notes
        fields = ['label']


class ListNotesSerializer(serializers.ModelSerializer):
    label = serializers.StringRelatedField(many=True, read_only=True)
    collaborator = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Notes
        fields = ['owner', 'title', 'description', 'label', 'collaborator', 'reminder']
        extra_kwargs = {'owner': {'read_only': True}, 'title': {'read_only': True}, 'content': {'read_only': True},
                        'reminder': {'read_only': True}}
