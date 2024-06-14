# urls.py

from django.urls import path

from .views import *

urlpatterns = [
    path('traductions/', get_traductions),
    path('langue/', ListLangue.as_view()),
    path('details_langue/<int:pk>', DetailLangue.as_view(),name='langue-detail'),
    path('search/', SearchListView.as_view()),
    path(' ', translate_text, name='translate-text'),
]
