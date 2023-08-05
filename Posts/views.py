from betenda_api.pagination import StandardResultsSetPagination
from rest_framework import  viewsets
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
        # Raises an exception if the key isn't present or is an empty string

        # Filter posts with the given tag name in the hashtags ManyToMany field
        try:
            posts = Post.objects.get(
                slug=slug)
        except:
            raise ResourceNotFound("The post was not found")
        
        serializer = Thread_CUD_Serializer(
            posts, context={'request': request})

        return send_response(serializer.data, "Post retrieved successfully")

    @action(detail=True, methods=['get'])
    def get_post_with_tag(self, request):
        tag = request.GET.get('tag')
        # Raises an exception if the key isn't present or is an empty string
        validate_key_value(tag, "Tag")

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

        serializer = Post_CUD_Serializer(
            data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)
        if parent:
            serializer.save(user=user, parent_id=parent_id)
        else:
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
