from rest_framework.response import Response
from rest_framework import generics
from .models import *
from .serializer import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions

from rest_framework import status
from . import client
from rest_framework.pagination import PageNumberPagination
import pickle
from rest_framework.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
import os

class TraductionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Vue pour la récupération des traductions
@login_required
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_traductions(request, format=None):
    try:
        # Retrieve and validate parameters
        langue_cible = request.query_params.get('langue')
        mot = request.query_params.get('mot')

        # Filter translations
        traductions = Traduction.objects.filter(langue=langue_cible)
        if mot:
            traductions = traductions.filter(motsfrancais=mot)

        # Pagination (optional)
        #traductions = self.paginate_queryset(traductions)

        # Serialize translations
        serializer = TraductionSerializer(traductions, many=True, context={'request': request})

        # Return response
        return Response(serializer.data)

    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Traduction.DoesNotExist:
        return Response({"error": "Traduction introuvable"}, status=status.HTTP_404_NOT_FOUND)

    except Exception:
       # Logger.error(f"Erreur inattendue: {e}")
        return Response({"error": "Une erreur interne est survenue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ListLangue(generics.ListAPIView):
    queryset = Langue.objects.all()
    serializer_class= LangueSerializer

#afficher les details sur une langue
class DetailLangue(generics.RetrieveAPIView):
    queryset = Langue.objects.all()
    serializer_class= LangueSerializer


class SearchListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        user = None
        if request.user.is_authenticated:
            user = request.user.username
        public = str(request.GET.get('public')) !='0'
        query = request.GET.get('q')

        if not query:
            return Response("Aucun mot trouvé", status=400)
        result = client.perform_search(query
        )
        return Response(result, status=200)




import joblib  # Si vous avez sauvegardé votre modèle avec joblib

@api_view(['GET', 'POST'])
def translate_text(request):
    if request.method == 'GET':
        text = request.GET.get('text', '')
        source_lang = request.GET.get('source_lang', 'fr')
        target_lang = request.GET.get('target_lang', 'en')
        
        # Charger le modèle depuis model.pkl
        model_path = '/home/davy/Desktop/emane bile/emane/UIECC S8/lm/LM/model.pkl'  # Chemin vers votre modèle
        model = joblib.load(model_path)  # Charger le modèle avec joblib
        
        # Effectuer la traduction
        translated_text = translate_with_model(model, text, source_lang, target_lang)
        
        return JsonResponse({"translated_text": translated_text}, status=200)
    
    elif request.method == 'POST':
        # Logique pour les requêtes POST si nécessaire
        pass
    
    return JsonResponse({"error": "Only GET requests are allowed for this endpoint."}, status=405)

def translate_with_model(model, text, source_lang, target_lang):
    # Exemple de fonction pour la traduction avec votre modèle
    # Ici, vous devez implémenter la logique de traduction en utilisant votre modèle
    # Remarque : Ceci est un exemple fictif, adaptez-le à votre modèle réel
    translated_text = model.translate(text, source_lang, target_lang)
    return translated_text
