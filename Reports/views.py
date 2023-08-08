from Articles.models import Article
from Comments.models import Comment
from Contributions.models import Poem
from django.contrib.contenttypes.models import ContentType
from HashTags.models import HashTag
from Posts.models import Post
from Reports.models import Report
from Reports.serializers import Report_Create_Serializer, Report_GET_Serializer
from rest_framework import generics
from Users.models import User

from betenda_api.methods import (BadRequest, ResourceNotFound, send_response,
                                 validate_key_value)
from betenda_api.pagination import StandardResultsSetPagination


# Create your views here.
class Report_Create_View(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = Report_Create_Serializer
    
    def post(self, request):
        resource_id = request.GET.get('resource_id')
        resource_type = request.GET.get('resource_type')

        user = request.user

        # rases exception if key isn't present or is empty ""
        validate_key_value(resource_id, "resource_id")
        validate_key_value(resource_type, "resource_type")

        # reportable resource types
        resource_type_mapping = {
            "article": Article,
            "comment": Comment,
            "post": Post,
            "poem": Poem,
            "user": User,
            "hashtag": HashTag,
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
            return send_response(serializer.data, "Reported successfully", 201)
        raise BadRequest(serializer.errors)
    


class Reports_List_View(generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = Report_GET_Serializer
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        resource_id = request.GET.get('resource_id')
        resource_type = request.GET.get('resource_type')

        validate_key_value(resource_id, "resource_id")
        validate_key_value(resource_type, "resource_type")

        comments = self.queryset.filter(
            content_type__model=resource_type, object_id=resource_id)

        # Manually apply pagination
        paginator = self.pagination_class()
        paginated_comments = paginator.paginate_queryset(comments, request)

        serializer = self.serializer_class(paginated_comments, many=True, context = {'request':request})
        return paginator.get_paginated_response(serializer.data)