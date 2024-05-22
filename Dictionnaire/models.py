from django.db import models

# Create your models here.
# models.py

class Langue(models.Model):
    id_langue = models.AutoField(primary_key=True)
    nom_langue = models.CharField(max_length=255)
    def __str__(self):
        return self.nom_langue

class MotsFrancais(models.Model):
    id_mots = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255, unique=True)
    image=models.FileField( upload_to='image/', null=True)
    def __str__(self):
        return self.nom
    
class Traduction(models.Model):
    id_trad = models.AutoField(primary_key=True)
    langue = models.ForeignKey(Langue, on_delete=models.CASCADE)
    motsfrancais = models.ForeignKey(MotsFrancais, on_delete=models.CASCADE)
    traduction = models.CharField(max_length=255, blank=True)
    audio_traduction = models.FileField(upload_to='audio/', max_length=255)
    expression = models.CharField(max_length=255, blank=True)
    audio_expression = models.FileField(upload_to='audio/', max_length=255)
    def __str__(self):
        return self.traduction

    def is_public(self)-> bool:
        return self.public