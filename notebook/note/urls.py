from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('mynotes/', views.MyNotesByUserListView.as_view(), name='mynotes'),
    path('mynote/<int:pk>', views.NoteByUserDetailView.as_view(), name='mynote'),
    path('mynotes/new', views.NoteByUserCreateView.as_view(), name='my-new'),
    path('mynotes/<int:pk>/update', views.NoteByUserUpdateView.as_view(), name='my-note-update'),
    path('mynotes/<int:pk>/delete', views.NoteByUserDeleteView.as_view(), name='my-note-delete'),
]