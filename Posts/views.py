from HashTags.models import UserHashtag
from Posts.notify import reply_to_comment_notification
from betenda_api.pagination import StandardResultsSetPagination
from rest_framework import  filters, generics, viewsets
from rest_framework.views import APIView
from betenda_api.methods import BadRequest, PermissionDenied, ResourceNotFound, send_response, validate_key_value
from rest_framework.decorators import action
from .models import Post
from .serializers import Post_CUD_Serializer, Thread_CUD_Serializer


class Post_List_GET_View(viewsets.ModelViewSet):
    '''
    Post list view
    '''
    queryset = Post.objects.filter(parent=None).select_related('user')
    @action(detail=True, methods=['get'])
    def list(self, request):
        posts = self.queryset.all().prefetch_related('reactions', 'post_parent')
        serializer = Post_CUD_Serializer(
            posts, many=True, context={'request': request})
        pagination_class = StandardResultsSetPagination()
        paginated_posts = pagination_class.paginate_queryset(
            serializer.data, request)

        return pagination_class.get_paginated_response(paginated_posts)
    
    @action(detail=True, methods=['get'])
    def get_user_posts(self, request):
        username = request.GET.get('username')
        # Raises an exception if the key isn't present or is an empty string
        validate_key_value(username, "username") 

        posts = self.queryset.filter(user__user_name=username).prefetch_related('reactions', 'post_parent')
        serializer = Post_CUD_Serializer(
            posts, many=True, context={'request': request})
        pagination_class = StandardResultsSetPagination()
        paginated_posts = pagination_class.paginate_queryset(
            serializer.data, request)

        return pagination_class.get_paginated_response(paginated_posts)

    @action(detail=True, methods=['get'])
    def get_post(self, request, slug):
        try:
            post = Post.objects.get(
                slug=slug)
        except:
            raise ResourceNotFound("The post was not found")

        tags = post.hashtags.all()
        for tag in tags:
            usertags, created = UserHashtag.objects.get_or_create(hashtag=tag, user=request.user)
            usertags.score += 1
            usertags.save()

        serializer = Thread_CUD_Serializer(
            post, context={'request': request})

        return send_response(serializer.data, "Post retrieved successfully")

    @action(detail=True, methods=['get'])
    def get_post_with_tag(self, request):
        tag = request.GET.get('tag')
        # Raises an exception if the key isn't present or is an empty string
        validate_key_value(tag, "Tag")
        usertags, created = UserHashtag.objects.get_or_create(hashtag__tag=tag, user=request.user)
        usertags.score += 1
        usertags.save()
        # Filter posts with the given tag name in the hashtags ManyToMany field
        posts = self.queryset.prefetch_related(
            'reactions', 'post_parent', 'hashtags').filter(hashtags__tag=tag)
        serializer = Post_CUD_Serializer(
            posts, many=True, context={'request': request})
        # Apply pagination to the queryset using StandardPagination
        pagination_class = StandardResultsSetPagination()
        paginated_posts = pagination_class.paginate_queryset(
            serializer.data, request)
        return pagination_class.get_paginated_response(paginated_posts)

    @action(detail=True, methods=['get'])
    def get_post_replies(self, request):
        parent = request.GET.get('parent')
        # Raises an exception if the key isn't present or is an empty string
        validate_key_value(parent, "parent ID")

        # Filter posts with the given tag name in the hashtags ManyToMany field
        posts = Post.objects.filter(parent=parent).prefetch_related(
            'reactions', 'post_parent', 'hashtags')
        serializer = Post_CUD_Serializer(
            posts, many=True, context={'request': request})
        # Apply pagination to the queryset using StandardPagination
        pagination_class = StandardResultsSetPagination()
        paginated_posts = pagination_class.paginate_queryset(
            serializer.data, request)
        return pagination_class.get_paginated_response(paginated_posts)
    # an algorism to query the feed would be great


class Post_CUD_View(APIView):
    '''
    Post create, update, delete view
    '''
    queryset = Post.objects.all()
    serializer_class = Post_CUD_Serializer

    def post(self, request, *args, **kwargs):
        user = request.user
        parent_id = request.GET.get('parent_id')
        parent = validate_key_value(
            parent_id, "parent ID", raise_exception=False)
        try:
            parent_object = Post.objects.get(id=parent_id)
        except:
            parent_object = None

        serializer = Post_CUD_Serializer(
            data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)
        if parent_object:
            saved = serializer.save(user=user, parent_id=parent_id)
            response_serializer = Thread_CUD_Serializer(saved, context={'request': request})
            # if the user is replying to him self no need to send a notification
            if not user == parent_object.user:
                reply_to_comment_notification(instance=response_serializer.instance, post=parent_object, request=request)
        else:
            saved = serializer.save(user=user)
            response_serializer = Post_CUD_Serializer(saved, context={'request': request})
        return send_response(response_serializer.data, "Post created successfully", 201)

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
        id = request.GET.get('id')
        # rases exception if key isn't present or is empty ""
        validate_key_value(id, "ID")

        try:
            instance = Post.objects.get(id=id)
        except:
            raise ResourceNotFound("Post was not found")

        if user.id != instance.user_id:
            raise PermissionDenied("You are not allowed to update this post")

        instance.delete()
        return send_response(None, "Post deleted successfully")

class Post_Search_View(generics.ListAPIView):
    queryset = Post.objects.all().select_related('user').prefetch_related('reactions', 'post_parent')
    serializer_class  = Post_CUD_Serializer
    filter_backends = [filters.SearchFilter]   
    search_fields = ['@content', '^hashtags__tag', '=hashtags__tag', 'user__first_name', 'user__last_name', 'user__user_name']