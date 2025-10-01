from django.shortcuts import render, get_object_or_404
from .models import Cours

def accueil(request):
    derniers_cours = Cours.objects.prefetch_related('liens').all()[:10]
    return render(request, 'accueil.html', {'cours': derniers_cours})

def detail_cours(request, id):
    cours = get_object_or_404(Cours.objects.prefetch_related('liens'), id=id)
    
    # Organiser les liens par type
    liens_par_type = {}
    for lien in cours.liens.all():
        if lien.type_lien not in liens_par_type:
            liens_par_type[lien.type_lien] = []
        liens_par_type[lien.type_lien].append(lien)
    
    return render(request, 'detail_cours.html', {
        'cours': cours,
        'liens_par_type': liens_par_type
    })