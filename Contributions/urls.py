from django.urls import path
from .views import Language_CUD_APIView, Poem_List_APIView, Saying_CU_APIView, Sentence_CU_APIView, Poem_GCU_APIView, Word_CU_APIView

urlpatterns = [
    path('langs', Language_CUD_APIView.as_view(),
         name="language_add_update_delete_view"),
    path('word', Word_CU_APIView.as_view(),
         name="word_add_update_delete_view"),
    path('poem', Poem_GCU_APIView.as_view(),
         name="poem_add_update_delete_view"),
    path('poem/<slug:slug>', Poem_GCU_APIView.as_view(),
         name="poem_get_delete_view"),
    path('poems', Poem_List_APIView.as_view(),
         name="poems_list_delete_view"),
    path('saying', Saying_CU_APIView.as_view(),
         name="saying_add_update_delete_view"),
    path('sentence', Sentence_CU_APIView.as_view(),
         name="sentence_add_update_delete_view"),
]