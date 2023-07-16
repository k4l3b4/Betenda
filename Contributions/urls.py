from django.urls import path
from .views import Language_CUD_APIView, Saying_CUD_APIView, Sentence_CUD_APIView, Poem_CUD_APIView, Word_CUD_APIView

urlpatterns = [
    path('lang', Language_CUD_APIView.as_view(),
         name="language_add_update_delete_view"),
    path('word', Word_CUD_APIView.as_view(),
         name="word_add_update_delete_view"),
    path('poem', Poem_CUD_APIView.as_view(),
         name="poem_add_update_delete_view"),
    path('saying', Saying_CUD_APIView.as_view(),
         name="saying_add_update_delete_view"),
    path('sentence', Sentence_CUD_APIView.as_view(),
         name="sentence_add_update_delete_view"),
]
