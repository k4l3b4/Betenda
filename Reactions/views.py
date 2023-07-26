from Articles.models import Article
from Comments.models import Comment
from betenda_api.methods import ServerError
from betenda_api.methods import compare_emojis
from Contributions.models import Poem, Saying
from Posts.models import Post
from Reactions.models import Reaction
from rest_framework.views import APIView
from Reactions.serializers import ReactionSerializer
from betenda_api.methods import BadRequest, ResourceNotFound, send_response, validate_key_value
from django.contrib.contenttypes.models import ContentType


class Reaction_CREATE_View(APIView):
    serializer_class = ReactionSerializer

    def post(self, request):
        try:
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
            if resource_type == "post" or resource_type == "comment" or not reaction and reaction != '❤️':
                data = {
                    'reaction': '❤️'
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
                # Get the existing reaction for the same user and content
                existing_reaction = Reaction.objects.get(
                    user=user, content_type=content_type, object_id=resource_id)
                serializer = self.serializer_class(
                    data=data, instance=existing_reaction)
            except Reaction.DoesNotExist:
                existing_reaction = None
                serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                # If the reaction is the same as the previous one, delete the reaction
                if resource_type == "post" or resource_type == "comment" and existing_reaction:
                    if existing_reaction and compare_emojis(existing_reaction.reaction, reaction):
                        existing_reaction.delete()
                        return send_response(None, 'Reaction deleted successfully')

                    serializer.save(content_object=instance, user=user,
                                    content_type=content_type)
                    return send_response(serializer.data, "Reacted successfully", 201)
                
                serializer.save(content_object=instance, user=user,
                                content_type=content_type)
                return send_response(serializer.data, "Reacted successfully", 201)
            raise BadRequest(serializer.errors)
        except:
          return ServerError("There was an error on our side")
