"""
models.py

This file contains the models used in the Django project.

The models are defined using the Django model framework, which provides an
object-relational mapping (ORM) between the database and Python objects.

The models are defined in the following classes:

- Langue: represents a language in the system
- MotsFrancais: represents a set of French words in the system
- Traduction: represents a translation of a French word into a different language

The relationships between the models are defined using foreign key fields.

The models are defined in the models.py file to keep the core of the application
decoupled from the views and templates.
"""
from django.db import models


class Langue(models.Model):
    """
    Langue class

    This class represents a language in the system.

    Attributes:
        id_langue (int): primary key
        nom_langue (str): name of the language
    """
    id_langue = models.AutoField(primary_key=True)
    nom_langue = models.CharField(max_length=255)


class MotsFrancais(models.Model):
    """
    MotsFrancais class

    This class represents a set of French words in the system.

    Attributes:
        id_mots (int): primary key
        nom (str): French word
    """
    id_mots = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)


class Traduction(models.Model):
    """
    Traduction class

    This class represents a translation of a French word into a different language.

    Attributes:
        id_trad (int): primary key
        langue (Langue): language of the translation
        motsfrancais (MotsFrancais): set of French words translated
        audio (FileField): audio file of the translation
        traduction (str): translation of the French words
    """
    id_trad = models.AutoField(primary_key=True)
    langue = models.ForeignKey(Langue, on_delete=models.CASCADE)
    motsfrancais = models.ForeignKey(MotsFrancais, on_delete=models.CASCADE)
    audio = models.FileField(upload_to=audio, max_length=255)
    traduction = models.CharField(max_length=255, blank=True)