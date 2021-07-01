from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('notes/', views.user_notes, name='user_notes'),                                    # List user's all notes.
    path('notes/<int:id>/', views.user_note_detail, name='user_note_detail'),               # View a note detail.
    path('notes/add/', views.user_add_note, name='user_add_note'),                          # Add a note.
    path('notes/edit/<int:id>/', views.user_edit_note, name='user_edit_note'),              # Edit a note.
    path('notes/delete/<int:id>/', views.user_delete_note, name='user_delete_note'),        # Delete a note.
    path('notes/gallery/<int:id>/', views.user_notes_gallery, name='user_notes_gallery'),   # Quick Gallery.
    path('comments/', views.user_comments, name='user_comments'),                           # List user's all comments.
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
]