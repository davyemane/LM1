import algoliasearch_django as algoliasearch

from .models import Traduction
from algoliasearch_django.decorators import register

#algoliasearch.register(Traduction)


from algoliasearch_django import AlgoliaIndex

@register(Traduction)

class TraductionIdex(AlgoliaIndex):
    fields = ['motsfrancais', 'traduction', 'expression']

    settings = {
        'attributesToRetrieve': ['motsfrancais', 'traduction', 'expression'],
        'attributesToHighlight': ['motsfrancais', 'traduction', 'expression'],
        'attributesToSnippet': ['motsfrancais', 'traduction', 'expression'],
        'searchableAttributes': ['motsfrancais', 'traduction', 'expression'],
        #'attributesForFaceting':['user', 'public']
    }
