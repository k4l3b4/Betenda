from Articles.models import Article
from Comments.models import Comment
from Contributions.models import Poem, Saying
from Posts.models import Post
from Reactions.models import Reaction
from rest_framework.views import APIView
from Reactions.serializers import ReactionSerializer
from betenda_api.methods import BadRequest, ResourceNotFound, send_response, validate_key_value
from django.contrib.contenttypes.models import ContentType


class Reaction_Create_View(APIView):
    serializer_class = ReactionSerializer

    def post(self, request):
        resource_id = request.GET.get('resource_id')
        resource_type = request.GET.get('resource_type')
        data = request.data.copy()
        user = request.user
        reaction = data.get('reaction', None)

        validate_key_value(resource_type, "resource_type")
        validate_key_value(resource_id, "resource_id")

        resource_type_mapping = {
            "article": Article,
            "comment": Comment,
            "poem": Poem,
            "post": Post,
            "saying": Saying,
        }

        # override the data if the resource_type is a post or a comment
        if resource_type == "post" or resource_type == "comment" and reaction != '❤':
            data = {
                'reaction': '❤'
            }

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
            duplicate = Reaction.objects.get(
                user=user, content_type=content_type, object_id=resource_id)
            serializer = self.serializer_class(data=data)
            if duplicate.reaction == reaction:
                duplicate.delete()
                return send_response(None, 'Reaction deleted successfully')

            if serializer.is_valid():
                serializer.update(duplicate, serializer.validated_data)
                return send_response(serializer.data, 'Reaction updated successfully')
            raise BadRequest(serializer.errors)
        except Reaction.DoesNotExist:
            pass

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(content_object=instance, user=user,
                            content_type=content_type)
            return send_response(serializer.data, "Reacted successfully", 201)
        raise BadRequest(serializer.errors)