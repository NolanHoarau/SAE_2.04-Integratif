from django.db import models

class Capteur(models.Model):
    nom = models.CharField(max_length=100)
    emplacement = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class Donnee(models.Model):
    capteur = models.ForeignKey(Capteur, on_delete=models.CASCADE, related_name='donnees')
    valeur = models.FloatField()
    horodatage = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.capteur.nom} - {self.horodatage}"
from django.db import models
