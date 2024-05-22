from logging import Logger
from rest_framework.response import Response
from rest_framework import generics
from .models import *
from .serializer import *
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions

from rest_framework import status
from . import client
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
import pickle
from easynmt import EasyNMT
from django.views.generic import list
from rest_framework.exceptions import ValidationError
from django.contrib.auth.decorators import login_required


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

@api_view(['GET', 'POST'])# Corrected decorator usage with list of methods
def translate_text(request):
    # with open("model.pkl", "rb") as pickle_in:  # Proper file opening and closing
    #     translator = pickle.load(pickle_in)

    translator = EasyNMT('opus-mt')

    if request.method == 'POST':
        text = request.POST.get('text')
        translated_text = translator.translate(text, source_lang='fr', target_lang='en')
        print("tranlated",translated_text)
        return Response(translated_text, status=200)
    
    if request.method == 'GET':
        text = request.GET.get('text')
        translated_text = translator.translate(text, source_lang='fr', target_lang='ln')
        return Response({"translated_text": translated_text}, status=200)


    # Handle non-POST requests with an appropriate response
    return Response({"error": "Only POST requests are allowed for this endpoint."}, status=405)