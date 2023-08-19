from betenda_api.methods import validate_key_value
from rest_framework import generics, filters
from rest_framework.views import APIView
from django.db.models import Count
from betenda_api.methods import (BadRequest, PermissionDenied,
                                 ResourceNotFound, check_user_permissions,
                                 send_response)
from betenda_api.pagination import StandardResultsSetPagination

from .models import Article
from .serializers import (ArticleGetSerializer, ArticleListSerializer,
                          ArticleSerializer)


# Create your views here.
class Article_List_View(generics.ListAPIView):
    queryset = Article.objects.filter(status="PUBLISHED").prefetch_related('reactions')
    serializer_class = ArticleListSerializer
    pagination_class = StandardResultsSetPagination

class Article_Trending_View(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        # annotate each article with the total number of reactions they have
        queryset = Article.objects.filter(status="PUBLISHED").annotate(
            total_reactions=Count('reactions')
        ).prefetch_related('reactions')

        # order the articles by the total number of reactions in descending order
        queryset = queryset.order_by('-total_reactions')

        # return the top 5 articles
        return queryset[:5]
    

class Article_Get_View(generics.RetrieveAPIView):
    queryset = Article.objects.filter(status="PUBLISHED")
    serializer_class = ArticleGetSerializer

    def get(self, request, slug, *args, **kwargs):
        try:
            article = self.queryset.get(slug=slug)
        except:
            raise ResourceNotFound("The article was not found")
        serializer = ArticleGetSerializer(article, context={'request':request})
        return send_response(serializer.data, "Article retrieved successfully")


class Article_CUD_View(APIView):
    '''
    Article create, update, delete view
    '''
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        user_id = str(user.id)
        data = request.data.copy()
        authors = data.get('authors', None)
        if authors:
            authors_list = [user_id] + [author.strip()
                                        for author in authors.split(',')]
        else:
            authors_list = [user_id]
        groups = ['Admin']
        perms = ['Articles.add_article']
        passable_data = {
            "title": data.get('title', None),
            "desc": data.get('desc', None),
            "body": data.get('body', None),
            "image": data.get('image', None),
            "status": data.get('status', None),
            "featured": data.get('featured', None),
            "authors": authors_list,
        }
        if check_user_permissions(user=user, groups=groups, perms=perms):
            serializer = ArticleSerializer(data=passable_data)
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response(serializer.data, "Article created successfully", 201)
        raise PermissionDenied("You don't have permission for this action")


    def patch(self, request, *args, **kwargs):
        id = request.GET.get('id')
        validate_key_value(id, "ID")
        user = request.user
        user_id = str(user.id)
        data = request.data.copy()
        authors = request.data.get('authors', None)
        if authors:
            authors_list = [user_id] + [author.strip()
                                        for author in authors.split(',')]
        else:
            authors_list = [user_id]
        groups = ['Admin']
        perms = ['Articles.change_article']
        passable_data = {
            "title": data.get('title', None),
            "desc": data.get('desc', None),
            "body": data.get('body', None),
            "image": data.get('image', None),
            "status": data.get('status', None),
            "featured": data.get('featured', None),
            "authors": authors_list,
        }
        passable_data = {
            key: value
            for key, value in passable_data.items()
            if value is not None
        }
        print(passable_data)
        try:
            instance = Article.objects.get(id=id)
        except:
            raise ResourceNotFound("Article was not found")

        # check if the user is the main author or is Admin/has permission to edit articles
        if user.id == instance.authors.first().id or check_user_permissions(user=user, groups=groups, perms=perms):
            serializer = ArticleSerializer(instance=instance,
                                        data=passable_data, partial=True, context={'request': request})
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response(serializer.data, "Article updated successfully")

        raise PermissionDenied("You don't have permission for this action")


    def delete(self, request, *args, **kwargs): 
        user = request.user
        groups = ['Admin']
        perms = ['Articles.delete_article']
        id = request.GET.get('id')
        validate_key_value(id, "ID")
        
        try:
            instance = Article.objects.get(id=id)
        except:
            raise ResourceNotFound("Article was not found")
        # check if the user is the main author or is Admin/has permission to delete articles
        if instance.authors.first() and user.id == instance.authors.first().id or check_user_permissions(user=user, groups=groups, perms=perms):
            instance.delete()
            return send_response(None, "Article deleted successfully")
        raise PermissionDenied("You don't have permission for this action")



class Article_Search_View(generics.ListAPIView):
    '''
    Search filter
    '''
    queryset = Article.objects.filter(status="PUBLISHED").prefetch_related('reactions')
    serializer_class  = ArticleGetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['@title', '@desc', '^hashtags__tag', '=hashtags__tag', 'authors__first_name', 'authors__last_name', 'authors__user_name']