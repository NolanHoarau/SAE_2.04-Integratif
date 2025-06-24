from django.shortcuts import render
from .models import Donnee


def messages_mqtt(request):
    nom = request.GET.get("nom", "")
    date = request.GET.get("date", "")

    donnees = Donnee.objects.all()

    if nom:
        donnees = donnees.filter(nom__icontains=nom)

    if date:
        donnees = donnees.filter(date__date=date)  # .date pour ne garder que la partie date

    return render(request, "donnees/messages_mqtt.html", {"donnees": donnees})
