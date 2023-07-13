from rest_framework.views import APIView

from betenda_api.methods import BadRequest, PermissionDenied, ResourceNotFound, send_response
from .models import Post
from .serializers import Post_CUD_Serializer


class Post_CUD_View(APIView):
    '''
    Post create, update, delete view
    '''
    query_set = Post.objects.all()
    serializer_class = Post_CUD_Serializer

    def post(self, request, *args, **kwargs):
        user = request.user

        serializer = Post_CUD_Serializer(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)
        serializer.save(user=user)
        return send_response(serializer.data, "Post created successfully", 201)

    def patch(self, request, *args, **kwargs):
        user = request.user

        try:
            id = request.data['id']
        except:
            raise BadRequest(
                "Needed information was not included: resource ID")

        try:
            instance = Post.objects.get(id=id)
        except:
            raise ResourceNotFound("Post was not found")

        if user.id != instance.user_id:
            raise PermissionDenied("You are not allowed to update this post")

        serializer = Post_CUD_Serializer(instance=instance,
                                         data=request.data, partial=True)
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)
        serializer.save()
        return send_response(serializer.data, "Post updated successfully")

    def delete(self, request, *args, **kwargs):
        user = request.user

        try:
            id = request.data['id']
        except:
            raise BadRequest(
                "Needed information was not included: resource ID")

        try:
            instance = Post.objects.get(id=id)
        except:
            raise ResourceNotFound("Post was not found")

        if user.id != instance.user_id:
            raise PermissionDenied("You are not allowed to update this post")

        instance.delete()
        return send_response(None, "Post deleted successfully")
