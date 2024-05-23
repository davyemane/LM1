# Importation des modules nécessaires
from rest_framework import serializers
from .models import *

# Création du sérialiseur LangueSerializer
class LangueSerializer(serializers.ModelSerializer):
    # Définition des champs à sérialiser
    urlDetails = serializers.HyperlinkedIdentityField(view_name="langue-detail", lookup_field = "pk")
    #traduction = serializers.HyperlinkedIdentityField(view_name="langue-traduction", lookup_field = "langue")
    class Meta:
        model = Langue
        fields = ["id_langue","nom_langue","urlDetails"]

# Création du sérialiseur MotsFrancaisSerializer
class MotsFrancaisSerializer(serializers.ModelSerializer):
    # Définition des champs à sérialiser
    #nom = serializers.CharField(source='*')
    class Meta:
        model = MotsFrancais
        fields = ['id_mots', 'nom','image']

# Création du sérialiseur TraductionSerializer
class TraductionSerializer(serializers.ModelSerializer):
    # Définition des champs à sérialiser
    langue = LangueSerializer()
    motsfrancais = MotsFrancaisSerializer()

    class Meta:
        model = Traduction
        fields = ['id_trad', 'langue', 'motsfrancais', 'traduction', 'audio_traduction', 'expression', 'audio_expression']

class Traductions(serializers.ModelSerializer):
    # Définition des champs à sérialiser
    langue = LangueSerializer()
    motsfrancais = MotsFrancaisSerializer()

    class Meta:
        fields = ['text', 'source_lang',  'target_lang']
