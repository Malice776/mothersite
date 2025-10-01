from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import Cours, LienCours


class LienCoursInline(admin.TabularInline):
    """
    Permet d'ajouter/modifier plusieurs liens directement 
    depuis la page de création/édition d'un cours
    """
    model = LienCours
    extra = 3  # Nombre de formulaires vides affichés par défaut
    fields = ['type_lien', 'titre', 'url', 'description', 'ordre']
    
    # Rendre les champs de description plus petits
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 60})},
    }


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    """
    Configuration simplifiée de l'admin pour les cours
    """
    # Ce qui s'affiche dans la liste des cours
    list_display = ['titre', 'date_ajout', 'nombre_liens']
    
    # Filtres sur le côté
    list_filter = ['date_ajout']
    
    # Barre de recherche
    search_fields = ['titre', 'description', 'contenu']
    
    # Date hiérarchique pour naviguer par date
    date_hierarchy = 'date_ajout'
    
    # Champs en lecture seule
    readonly_fields = ['date_ajout', 'date_modification']
    
    # Ajouter les liens inline
    inlines = [LienCoursInline]
    
    # Organisation des champs en sections
    fieldsets = (
        ('📝 Informations principales', {
            'fields': ('titre', 'description'),
            'description': 'Informations de base sur le cours'
        }),
        ('📄 Contenu détaillé', {
            'fields': ('contenu',),
            'classes': ('wide',),
            'description': 'Contenu complet du cours (optionnel)'
        }),
        ('📅 Dates', {
            'fields': ('date_ajout', 'date_modification'),
            'classes': ('collapse',),  # Section repliable
        }),
    )
    
    # Rendre les champs texte plus grands
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'cols': 80})},
    }
    
    # Méthode personnalisée pour afficher le nombre de liens
    @admin.display(description='Liens')
    def nombre_liens(self, obj):
        count = obj.liens.count()
        if count == 0:
            return '❌ Aucun lien'
        elif count == 1:
            return '✅ 1 lien'
        else:
            return f'✅ {count} liens'


@admin.register(LienCours)
class LienCoursAdmin(admin.ModelAdmin):
    """
    Admin pour gérer les liens individuellement (optionnel)
    """
    list_display = ['titre', 'cours', 'type_lien', 'ordre', 'voir_url']
    list_filter = ['type_lien', 'cours']
    search_fields = ['titre', 'url', 'description', 'cours__titre']
    list_editable = ['ordre']  # Permet de modifier l'ordre directement dans la liste
    
    # Organisation des champs
    fieldsets = (
        ('🔗 Informations du lien', {
            'fields': ('cours', 'titre', 'url', 'type_lien')
        }),
        ('📝 Détails', {
            'fields': ('description', 'ordre'),
        }),
    )
    
    # Méthode pour afficher un aperçu de l'URL
    @admin.display(description='URL')
    def voir_url(self, obj):
        url = obj.url[:50] + '...' if len(obj.url) > 50 else obj.url
        return url


# Personnalisation du site d'administration
admin.site.site_header = "📚 Administration des Cours"
admin.site.site_title = "Gestion des Cours"
admin.site.index_title = "Bienvenue sur l'interface d'administration"