from django.db import models

class Cours(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    contenu = models.TextField(blank=True, help_text="Contenu détaillé du cours")
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ['-date_ajout']

    def __str__(self):
        return self.titre


class LienCours(models.Model):
    TYPE_CHOICES = [
        ('video', 'Vidéo'),
        ('exercice', 'Exercice'),
        ('document', 'Document'),
        ('ressource', 'Ressource externe'),
        ('autre', 'Autre'),
    ]
    
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='liens')
    titre = models.CharField(max_length=200)
    url = models.URLField()
    type_lien = models.CharField(max_length=20, choices=TYPE_CHOICES, default='autre')
    description = models.TextField(blank=True)
    ordre = models.IntegerField(default=0, help_text="Ordre d'affichage")

    class Meta:
        verbose_name = "Lien"
        verbose_name_plural = "Liens"
        ordering = ['ordre', 'id']

    def __str__(self):
        return f"{self.titre} ({self.cours.titre})"