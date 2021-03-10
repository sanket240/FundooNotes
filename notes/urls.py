from django.urls import path
from .views import NoteCreateView, NoteOperationsView, LabelCreate, \
    LabelOperationsView, AddCollaboratorForNotes, AddLabelsToNote, ListCollaboratorAPIView, ListLabelAPIView, \
    AddReminderToNotes, TrashNotes, SearchAPIView, ArchiveNotes

urlpatterns = [
    path('', NoteCreateView.as_view(), name="create"),
    path('<int:id>', NoteOperationsView.as_view(), name="notes"),
    path('label/', LabelCreate.as_view(), name="label"),
    path('label/<int:id>', LabelOperationsView.as_view(), name='labels'),
    path('collab/', AddCollaboratorForNotes.as_view(), name='collab'),
    path('note-label/', AddLabelsToNote.as_view(), name='add-label'),
    path('list-collaborator/', ListCollaboratorAPIView.as_view(), name='list-collab'),
    path('list-label/', ListLabelAPIView.as_view(), name='list-label'),
    path('reminder/', AddReminderToNotes.as_view(), name='reminder'),
    path('trash/', TrashNotes.as_view(),name="trash"),
    path('search/', SearchAPIView.as_view(), name="search"),
    path('archive/', ArchiveNotes.as_view(), name="archive"),

]
