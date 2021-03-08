from django.urls import path
from .views import NoteCreateView, NoteOperationsView, LabelCreate, \
    LabelOperationsView, AddCollaboratorForNotes, AddLabelsToNote, ListCollaboratorAPIView, ListLabelAPIView, \
    AddReminderToNotes,SendReminderEmail ,TrashNotes,SearchAPIView,ArchiveNotes# DeleteNoteView, UpdateNoteAPIView, DisplayNotes

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
    #path('get/', GetReminder.as_view(), name='reminder'),
    path('remmail/',SendReminderEmail.as_view()),
    path('trash/',TrashNotes.as_view()),
    path('search/',SearchAPIView.as_view()),
    path('archive/',ArchiveNotes.as_view())
]
