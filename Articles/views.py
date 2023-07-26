from betenda_api.methods import BadRequest,ServerError, PermissionDenied, ResourceNotFound, check_user_permissions, send_response
from rest_framework.views import APIView
from Articles.models import Article
from Articles.serializers import ArticleGetSerializer, ArticleSerializer
from betenda_api.pagination import StandardResultsSetPagination
from rest_framework import generics


# Create your views here.
class Article_List_View(generics.ListAPIView):
    queryset = Article.objects.filter(status="PUBLISHED")
    serializer_class = ArticleSerializer
    pagination_class = StandardResultsSetPagination


class Article_Get_View(generics.RetrieveAPIView):
    queryset = Article.objects.filter(status="PUBLISHED")
    serializer_class = ArticleGetSerializer

    def get(self, request, slug, *args, **kwargs):
        try:
            article = self.queryset.get(slug=slug)
        except:
            raise ResourceNotFound("The article was not found")
        serializer = ArticleGetSerializer(article)
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
            authors_list = None
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
            print(passable_data)
            serializer = ArticleSerializer(data=passable_data)
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response(serializer.data, "Article created successfully", 201)
        raise PermissionDenied("You don't have permission for this action")


    def patch(self, request, *args, **kwargs):
        user = request.user
        user_id = str(user.id)
        data = request.data.copy()
        authors = request.data.get('authors', None)
        if authors:
            authors_list = [user_id] + [author.strip()
                                        for author in authors.split(',')]
        else:
            authors_list = None
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
        try:
            id = request.data['id']
        except:
            raise BadRequest(
                "Needed information was not included: resource ID")

        try:
            instance = Article.objects.get(id=id)
        except:
            raise ResourceNotFound("Article was not found")

        # check if the user is the main author or is Admin/has permission to edit articles
        if user.id == instance.authors.first().id or check_user_permissions(user=user, groups=groups, perms=perms):
            serializer = ArticleSerializer(instance=instance,
                                        data=passable_data, partial=True)
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response(serializer.data, "Article updated successfully")

        raise PermissionDenied("You don't have permission for this action")


    def delete(self, request, *args, **kwargs): 
        user = request.user
        groups = ['Admin']
        perms = ['Articles.delete_article']
        try:
            id = request.data['id']
        except:
            raise BadRequest(
                "Needed information was not included: resource ID")
        try:
            instance = Article.objects.get(id=id)
        except:
            raise ResourceNotFound("Article was not found")
        # check if the user is the main author or is Admin/has permission to delete articles
        if instance.authors.first() and user.id == instance.authors.first().id or check_user_permissions(user=user, groups=groups, perms=perms):
            instance.delete()
            return send_response(None, "Article deleted successfully")
        raise PermissionDenied("You don't have permission for this action")
