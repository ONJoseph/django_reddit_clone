from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit, name='submit'),
    path('submission/<int:pk>/', views.submission_detail, name='submission_detail'),
    # Add the URL pattern for post_comment view
    path('post_comment/', views.post_comment, name='post_comment'),
]
