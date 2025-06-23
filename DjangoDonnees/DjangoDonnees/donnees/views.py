from django.shortcuts import render, get_object_or_404, redirect
from .models import Capteur
from .forms import CapteurForm

def liste_capteurs(request):
    capteurs = Capteur.objects.all()
    return render(request, 'donnees/liste_capteurs.html', {'capteurs': capteurs})

def details_capteur(request, id):
    capteur = get_object_or_404(Capteur, id=id)
    return render(request, 'donnees/details_capteur.html', {
        'capteur': capteur,
        'donnees': capteur.donnees.all()
    })

def modifier_capteur(request, id):
    capteur = get_object_or_404(Capteur, id=id)
    form = CapteurForm(request.POST or None, instance=capteur)
    if form.is_valid():
        form.save()
        return redirect('details_capteur', id=capteur.id)
    return render(request, 'donnees/modifier_capteur.html', {'form': form})
