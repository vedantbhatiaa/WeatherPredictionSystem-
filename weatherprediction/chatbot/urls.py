from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('process-message/', views.process_message, name='process_message'),
]