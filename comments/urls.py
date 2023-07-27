from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path(r'^update/(?P<comment_id>\d+)/$', views.update_comment, name='update_comment'),
]
