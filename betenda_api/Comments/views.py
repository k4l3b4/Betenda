from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework import generics
from .models import Comment
from .serializers import Comment_CUD_Serializer, Comment_GET_Serializer
from betenda_api.pagination import StandardResultsSetPagination
from betenda_api.methods import BadRequest, PermissionDenied, ResourceNotFound, send_response, validate_key_value
from Articles.models import Article
# Create your views here.


class Comment_CUD_View(APIView):
    serializer_class = Comment_CUD_Serializer

    def post(self, request):
        resource_id = request.GET.get('resource_id')
        resource_type = request.GET.get('resource_type')
        parent_id = request.GET.get('parent_id')

        user = request.user

        # rases exception if key isn't present or is empty ""
        validate_key_value(resource_id, "resource_id")

        if parent_id & parent_id != "":
            try:
                parent = Comment.objects.get(id=parent_id)
            except:
                raise ResourceNotFound("Parent comment not found")
        else:
            parent = None

        if resource_type == "article":
            try:
                instance = Article.objects.get(id=resource_id)
            except:
                raise ResourceNotFound("Article was not found")

            content_type = ContentType.objects.get_for_model(instance)

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(content_object=instance, user=user,
                                content_type=content_type, parent=parent)
                return send_response(serializer.data, "Commented successfully", 201)
            raise BadRequest(serializer.errors)
        raise BadRequest("Needed information was not included: resource_type")

    def patch(self, request):
        comment_id = request.GET.get('comment_id')
        user = request.user

        validate_key_value(comment_id, "comment_id")

        try:
            instance = Comment.objects.get(id=comment_id)
        except:
            raise ResourceNotFound("The resource not found")

        serializer = self.serializer_class(
            instance=instance, data=request.data, partial=True)
        if instance.user.id == user.id:
            if serializer.is_valid():
                serializer.save()
                return send_response(serializer.data, "Comment updated successfully")
            raise BadRequest(serializer.errors)
        raise PermissionDenied(
            "You are not allowed to perform this action")

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
    queryset = Comment.objects.filter(parent=None)
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        resource_id = request.GET.get('resource_id')
        resource_type = request.GET.get('resource_type')
        parent_id = request.GET.get('parent_id', None)

        validate_key_value(resource_id, "resource_id")
        validate_key_value(resource_type, "resource_type")

        comments = self.queryset.filter(
            content_type__model=resource_type, object_id=resource_id, parent_id=parent_id)

        # Manually apply pagination
        paginator = self.pagination_class()
        paginated_comments = paginator.paginate_queryset(comments, request)

        serializer = Comment_GET_Serializer(paginated_comments, many=True)
        return paginator.get_paginated_response(serializer.data)
