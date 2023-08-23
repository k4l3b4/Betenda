from django.db.models import Sum
from HashTags.models import UserHashtag
from rest_framework import filters

class PostTagFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        user_tags = UserHashtag.objects.filter(user=user)
        user_score_sum = user_tags.aggregate(Sum('score'))['score__sum'] or 0

        ranked_posts = []
        for post in queryset:
            post_tags = post.hashtags.all()
            for post_tag in post_tags:
                user_post_tag = UserHashtag.objects.filter(user=user, hashtag=post_tag).first()
                if user_post_tag:
                    tag_score_sum = sum([tag.score for tag in user_post_tag])

                    rank = (tag_score_sum * user_score_sum) / (tag_score_sum + user_score_sum + 1)

                    if tag_score_sum == 0:
                        rank = user_score_sum / 2

                    ranked_posts.append((post, rank))

        ranked_posts.sort(key=lambda x: x[1], reverse=True)
        return [post[0] for post in ranked_posts]
    



    # @action(detail=True, methods=['get'])
    # def list(self, request):
    #     filtered_posts = self.filter_queryset(self.queryset)

    #     posts = filtered_posts.prefetch_related('reactions', 'post_parent')
    #     serializer = Post_CUD_Serializer(
    #         posts, many=True, context={'request': request})
    #     pagination_class = StandardResultsSetPagination()
    #     paginated_posts = pagination_class.paginate_queryset(
    #         serializer.data, request)

    #     return pagination_class.get_paginated_response(paginated_posts)