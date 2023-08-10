from django.contrib.contenttypes.models import ContentType
from Contributions.models import Poem, Saying
from .notify import comment_notification
from rest_framework.decorators import action
from rest_framework import generics, viewsets
from .models import Comment
from .serializers import Comment_CUD_Serializer, Comment_GET_Serializer
from betenda_api.pagination import StandardResultsSetPagination
from betenda_api.methods import BadRequest, PermissionDenied, ResourceNotFound, send_response, validate_key_value
from Articles.models import Article
# Create your views here.


class Comment_CUD_View(viewsets.ModelViewSet):
    serializer_class = Comment_CUD_Serializer


    @action(detail=True, methods=['post'])
    def comment(self, request):
        resource_id = request.GET.get('resource_id')
        resource_type = request.GET.get('resource_type')

        user = request.user

        # rases exception if key isn't present or is empty ""
        validate_key_value(resource_id, "resource_id")
        validate_key_value(resource_type, "resource_type")

        # Commentable types
        resource_type_mapping = {
            "article": Article,
            "saying": Saying,
            "poem": Poem,
        }

        try:
            # trying to get the resource object
            model_class = resource_type_mapping[resource_type]
            instance = model_class.objects.get(id=resource_id)
        except KeyError:
            raise BadRequest("Invalid resource_type")
        except model_class.DoesNotExist:
            raise ResourceNotFound(
                f"{resource_type.capitalize()} was not found")

        content_type = ContentType.objects.get_for_model(instance)

        serializer = self.serializer_class(data=request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save(content_object=instance, user=user,
                            content_type=content_type)
            comment_notification(serializer.instance, request)
            return send_response(serializer.data, "Commented successfully", 201)
        raise BadRequest(serializer.errors)
    

    @action(detail=True, methods=['post'])
    def reply(self, request):
        resource_id = request.GET.get('resource_id')
        resource_type = request.GET.get('resource_type')
        parent = request.GET.get('parent')

        user = request.user

        # rases exception if key isn't present or is empty ""
        validate_key_value(resource_id, "resource_id")
        validate_key_value(resource_type, "resource_type")
        validate_key_value(parent, "parent_id")

        # Comment repliable types
        resource_type_mapping = {
            "article": Article,
            "saying": Saying,
            "poem": Poem,
        }
        try:
          parent_comment = Comment.objects.get(id=parent)
          top_comment = parent_comment.parent if parent_comment.parent else parent_comment
        except:
          raise ResourceNotFound("Comment not found")

        try:
            # trying to get the resource object
            model_class = resource_type_mapping[resource_type]
            instance = model_class.objects.get(id=resource_id)
        except KeyError:
            raise BadRequest("Invalid resource_type")
        except model_class.DoesNotExist:
            raise ResourceNotFound(
                f"{resource_type.capitalize()} was not found")

        content_type = ContentType.objects.get_for_model(instance)
            
        serializer = self.serializer_class(data=request.data, context = {'request':request})
        if serializer.is_valid():
            serializer.save(content_object=instance, user=user,
                            content_type=content_type, parent=top_comment, immediate_parent=parent_comment)
            # reformat the returned data to fit in the frontend
            return_serializer = Comment_GET_Serializer(serializer.instance, context = {'request': request})
            comment_notification(serializer.instance, request)
            return send_response(return_serializer.data, "Replied successfully", 201)
        raise BadRequest(serializer.errors)
    
    @action(detail=True, methods=['patch'])
    def update(self, request):
        comment_id = request.GET.get('comment_id')
        user = request.user

        validate_key_value(comment_id, "comment_id")

        try:
            instance = Comment.objects.get(id=comment_id)
        except:
            raise ResourceNotFound("The resource not found")

        serializer = self.serializer_class(
            instance=instance, data=request.data, partial=True, context = {'request':request})
        if instance.user.id == user.id:
            if serializer.is_valid():
                serializer.save()
                return send_response(serializer.data, "Comment updated successfully")
            raise BadRequest(serializer.errors)
        raise PermissionDenied(
            "You are not allowed to perform this action")

    @action(detail=True, methods=['delete'])
    def delete(self, request):
        comment_id = request.GET.get('comment_id')
        user = request.user

        validate_key_value(comment_id, "comment_id")

        try:
            instance = Comment.objects.get(id=comment_id)
        except:
            raise ResourceNotFound("The resource not found")
        
        if instance.user.id == user.id:
            instance.delete()
            return send_response(None, "Comment deleted successfully")
        raise PermissionDenied(
            "You are not allowed to perform this action")



class Comment_List_View(generics.ListAPIView):
    serializer_class = Comment_GET_Serializer
    queryset = Comment.objects.all()
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        resource_id = request.GET.get('resource_id')
        resource_type = request.GET.get('resource_type')
        parent_id = request.GET.get('parent_id', None)

        validate_key_value(resource_id, "resource_id")
        validate_key_value(resource_type, "resource_type")

        comments = self.queryset.filter(
            content_type__model=resource_type, object_id=resource_id, parent=parent_id)

        # Manually apply pagination
        paginator = self.pagination_class()
        paginated_comments = paginator.paginate_queryset(comments, request)

        serializer = Comment_GET_Serializer(paginated_comments, many=True, context = {'request':request})
        return paginator.get_paginated_response(serializer.data)