from rest_framework.response import Response
from rest_framework import generics
from .models import *
from .serializer import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from django.http import JsonResponse
from rest_framework import status
from . import client
import pickle
from rest_framework.exceptions import ValidationError
import os
from Dictionnaire import *

class TraductionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Vue pour la récupération des traductions
@api_view(['GET'])
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




from easynmt import EasyNMT

# Initialiser le traducteur EasyNMT une fois
model = EasyNMT('opus-mt')

@api_view(['GET', 'POST'])
def translate_text(request):
    if request.method in ['GET', 'POST']:
        text = request.GET.get('text', '') if request.method == 'GET' else request.POST.get('text', '')
        source_lang = request.GET.get('source_lang', '') if request.method == 'GET' else request.POST.get('source_lang', '')
        target_lang = request.GET.get('target_lang', '') if request.method == 'GET' else request.POST.get('target_lang', '')

        # Vérifier si le texte est une chaîne ou une liste de phrases
        if isinstance(text, str):
            # Traiter comme une seule phrase
            texts = [text]
        else:
            # Traiter comme plusieurs phrases
            texts = text

        try:
            # Effectuer la traduction
            translated_texts = model.translate(texts, source_lang=source_lang, target_lang=target_lang)
            if isinstance(text, str):
                # Retourner un seul texte traduit si l'entrée était une chaîne
                translated_text = translated_texts[0]
            else:
                # Retourner une liste de textes traduits si l'entrée était une liste
                translated_text = translated_texts

            return JsonResponse({"translated_text": translated_text}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Only GET and POST requests are allowed for this endpoint."}, status=405)
