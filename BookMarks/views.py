from django.contrib.contenttypes.models import ContentType
from Articles.models import Article
from Contributions.models import Poem
from Posts.models import Post
from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import BookMarkSerializer
from betenda_api.methods import BadRequest, ResourceNotFound, send_response, validate_key_value
from betenda_api.pagination import StandardResultsSetPagination

from .models import BookMark


# Create your views here.
class BookMark_LAD_View(viewsets.ModelViewSet):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer
    '''
    BookMark list view
    '''
    @action(detail=True, methods=['get'])
    def list(self, request):
        user = request.user
        posts = self.queryset.filter(user=user).select_related('content_type').prefetch_related('content_object')
        serializer = self.serializer_class(posts, many=True, context={'request': request})
        pagination_class = StandardResultsSetPagination()
        paginated_posts = pagination_class.paginate_queryset(
            serializer.data, request)
        return pagination_class.get_paginated_response(paginated_posts)
    

    @action(detail=True, methods=['post'])
    def add_or_delete(self, request, *args, **kwargs):
        resource_id = request.GET.get('resource_id')
        resource_type = request.GET.get('resource_type')
        user = request.user

        resource_type_mapping = {
            "article": Article,
            "poem": Poem,
            "post": Post,
        }

        validate_key_value(resource_id, "Resource ID")
        validate_key_value(resource_type, "Resource type")

        try:
            model_class = resource_type_mapping[resource_type]
            instance = model_class.objects.get(id=resource_id)
        except KeyError:
            raise BadRequest("Invalid resource_type")
        except model_class.DoesNotExist:
            raise ResourceNotFound(
                f"{resource_type.capitalize()} was not found")

        content_type = ContentType.objects.get_for_model(instance)
        
        try:
            bookmark = BookMark.objects.get(object_id=instance.id, user=user, content_type=content_type)
        except:
            bookmark = None

        if bookmark:
            bookmark.delete()
            return send_response(None, "BookMarked item deleted successfully", 201)
        else:
            try:
                BookMark.objects.create(content_object=instance, user=user, content_type=content_type)
            except:
                raise BadRequest("Failed to bookmark this resource")
        return send_response(None, "BookMarked successfully", 201)