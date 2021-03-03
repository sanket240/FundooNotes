from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, RetrieveAPIView, \
    GenericAPIView, RetrieveUpdateAPIView
from .models import Notes, Labels
from .serializers import NotesSerializer, LabelsSerializer, CollaboratorSerializer, AddLabelsToNoteSerializer, \
    ListNotesSerializer
from rest_framework import permissions, status, views
import logging
from psycopg2 import OperationalError
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse

logger = logging.getLogger('django')


class NoteCreateView(ListCreateAPIView):
    serializer_class = NotesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """
                This api is for creation of new notes
                @param request: title and description of notes
                @return: response of created notes
        """
        try:
            serializer.save(owner=self.request.user)
            logger.info("Note Created Successfully")
            return Response({'Message': 'Note Created Successfully'}, status=status.HTTP_200_OK)
        except OperationalError as e:
            logger.error(e)
            return Response({'Message': 'Failed to connect with the database'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(e)
            return Response({'Message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'Message': 'Failed to create new note'}, status=status.HTTP_400_BAD_REQUEST)

    # TOdo add responses
    def get_queryset(self):
        """ Get all notes of particular User """
        try:
            logger.info("Data Incoming from the database")
            return Notes.objects.filter(owner=self.request.user)
        except OperationalError as e:
            logger.error(e)
            return Response({'Message': 'Failed to connect with the database'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)


class NoteOperationsView(RetrieveUpdateDestroyAPIView):
    serializer_class = NotesSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def perform_destroy(self, instance):
        """
                   This api is for creation of new notes
                   @param request: ID of the notes
                   @return: response of deleted notes
        """
        try:
            instance.delete()
            logger.info("Note Deleted Successfully")
            return Response({'Message': 'Note is deleted permanently'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.error(e)
            return Response({'Message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        except OperationalError as e:
            logger.error(e)
            return Response({'Message': 'Failed to connect with the database'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'Message': 'Failed to delete new note,Please try again later'},
                            status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        """
                This api is for updating of new notes
                @param request: ID of the notes
                @return: response of updated notes
        """
        try:
            note = serializer.save()
            logger.info("Note Updated Successfully")
            return Response({'Message': 'Note Updated Successfully'}, status=status.HTTP_200_OK)
        except OperationalError as e:
            logger.error(e)
            return Response({'Message': 'Failed to connect with the database'}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            logger.error(e)
            return Response({'Message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'Message': 'Failed to update note'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """ Get all notes of particular User """
        try:
            logger.info("Data Incoming from the database")
            return Notes.objects.filter(owner=self.request.user)
        except OperationalError as e:
            logger.error(e)
            return Response({'Message': 'Failed to connect with the database'}, status=status.HTTP_400_BAD_REQUEST)


class LabelCreate(ListCreateAPIView):
    serializer_class = LabelsSerializer
    queryset = Labels.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        """
                  This api is for creation of new Label
                  @param request: name of label
                  @return: response of created labels
        """
        owner = self.request.user
        serializer.save(owner=owner)
        logger.info("Label Created")
        return Response({'success': 'New label is created!!'}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
                    This api is for getting list of all labels for paticular user

        """
        owner = self.request.user
        return self.queryset.filter(owner=owner)


class LabelOperationsView(RetrieveUpdateDestroyAPIView):
    serializer_class = LabelsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def perform_destroy(self, instance):
        """
                   This api is for creation of new labels
                   @param request: ID of the labels
                   @return: response of deleted labels
        """
        try:
            instance.delete()
            logger.info("Label Deleted Successfully")
            return Response({'Message': 'Label is deleted permanently'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.error(e)
            return Response({'Message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        except OperationalError as e:
            logger.error(e)
            return Response({'Message': 'Failed to connect with the database'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'Message': 'Failed to delete Label,Please try again later'},
                            status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        """
                This api is for updating of new Labels
                @param request: ID of the labels
                @return: response of updated labels
        """
        try:
            note = serializer.save()
            logger.info("Label Updated Successfully")
            return Response({'Message': 'Label Updated Successfully'}, status=status.HTTP_200_OK)
        except OperationalError as e:
            logger.error(e)
            return Response({'Message': 'Failed to connect with the database'}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            logger.error(e)
            return Response({'Message': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'Message': 'Failed to update label'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """ Get all labels for particular user """
        try:
            logger.info("Data Incoming from the database")
            return Labels.objects.filter(owner=self.request.user)
        except OperationalError as e:
            logger.error(e)
            return Response({'Message': 'Failed to connect with the database'}, status=status.HTTP_400_BAD_REQUEST)


class AddCollaboratorForNotes(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CollaboratorSerializer

    def get(self, request):
        note_id = request.data.get('note_id')
        return HttpResponse(Notes.objects.get(id=note_id))

    def put(self, request):
        note_id = request.data.get('note_id')
        note = Notes.objects.get(id=note_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        collaborator_email = serializer.validated_data['collaborator']
        try:
            collaborator = User.objects.get(email=collaborator_email)
        except:
            return Response({'User email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if collaborator == request.user:
            return Response({'Message': 'This email already exists!!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            note.collaborator.add(collaborator)
            note.save()
            return Response({'collaborator': collaborator_email}, status=status.HTTP_200_OK)


class AddLabelsToNote(GenericAPIView):
    """ API to add available labels to notes of requested user """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddLabelsToNoteSerializer

    def put(self, request):
        note_id = request.data.get('note_id')
        note = Notes.objects.get(id=note_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        label_name = serializer.validated_data['label']
        try:
            label = Labels.objects.get(name=label_name, owner=self.request.user)
        except Labels.DoesNotExist:
            label = Labels.objects.create(name=label_name, owner=self.request.user)
        note.label.add(label.id)
        note.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListCollaboratorAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()

    def get(self, request):
        user = request.user
        collaborated_users = []
        collaborator = Notes.objects.filter(collaborator__isnull=False)
        if collaborator:
            collaborator_list = collaborator.values('collaborator')
            for i in range(len(collaborator_list)):
                collab_id = collaborator_list[i]['collaborator']
                collab1 = User.objects.filter(id=collab_id)
                collab_email = collab1.values('email')
                collaborator_list[i].update(collab_email[0])
                collaborated_users = collaborated_users + [collaborator_list[i]]
                return Response({"Collaborated Users": collaborated_users}, status=200)
        else:
            logger.info("No such Note available to have any collabrator Added")
            return Response({"response": "No such Note available to have any collabrator Added"}, status=404)


class ListLabelAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LabelsSerializer
    queryset = Notes.objects.all()

    def get(self, request):
        user = request.user
        label_users = []
        labels = Notes.objects.filter(label__isnull=False)
        if labels:
            label_list = labels.values('label')
            for i in range(len(label_list)):
                Label_id = label_list[i]['label']
                label =Labels.objects.filter(id=Label_id)
                label_name = label.values('name')
                label_list[i].update(label_name[0])
                label_users = label_users + [label_list[i]]
                return Response({"Labels Attached To Notes": label_users}, status=200)
        else:
            logger.info("No such Note available to have any collabrator Added")
            return Response({"Error": "No Labels are attached to the notes"}, status=404)
