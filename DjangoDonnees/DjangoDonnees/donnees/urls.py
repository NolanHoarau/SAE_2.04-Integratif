from django.urls import path
from . import views

urlpatterns = [
    path('', views.messages_mqtt, name='messages_mqtt'),
]
