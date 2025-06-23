from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_capteurs, name='liste_capteurs'),
    path('capteur/<int:id>/', views.details_capteur, name='details_capteur'),
    path('capteur/<int:id>/modifier/', views.modifier_capteur, name='modifier_capteur'),
]
