from rest_framework.decorators import action
from betenda_api.pagination import StandardResultsSetPagination
from rest_framework import generics, viewsets
from RoadMaps.models import Goal
from betenda_api.methods import BadRequest, PermissionDenied, ResourceNotFound, check_user_permissions, send_response, validate_key_value
from rest_framework.views import APIView
from .serializers import GoalSerializer


# Create your views here.
class Goal_CUD_View(APIView):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()

    def post(self, request, *args, **kwargs):
        user = request.user
        groups = ['Admin']
        perms = ['RoadMaps.add_goal']

        if check_user_permissions(user=user, groups=groups, perms=perms):
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response(serializer.data, "Goal registered successfully", 201)
        raise PermissionDenied("You don't have permission for this action")

    def patch(self, request, *args, **kwargs):
        user = request.user
        groups = ['Admin']
        perms = ['RoadMaps.change_goal']

        id = request.GET.get('id')
        # rases exception if key isn't present or is empty ""
        validate_key_value(id, "ID")

        try:
            instance = Goal.objects.get(id=id)
        except:
            raise ResourceNotFound("The the goal was not found")

        if check_user_permissions(user=user, groups=groups, perms=perms):
            serializer = self.serializer_class(
                instance=instance, data=request.data)
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response(serializer.data, "Goal updated successfully", 201)
        raise PermissionDenied("You don't have permission for this action")

    def delete(self, request, *args, **kwargs):
        id = request.GET.get('id')
        # rases exception if key isn't present or is empty ""
        validate_key_value(id, "ID")

        user = request.user
        groups = ['Admin']
        perms = ['RoadMaps.delete_goal']
        try:
            instance = Goal.objects.get(id=id)
        except:
            raise ResourceNotFound("The goal was not found")

        if check_user_permissions(user=user, groups=groups, perms=perms):
            instance.canceled = True
            instance.save()
            return send_response(None, "Goal canceled successfully")
        raise PermissionDenied("You don't have permission for this action")

class Goal_STATE_View(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def achieved(self, request, pk=None):
        try:
            goal = Goal.objects.get(id=pk, achieved=False)
        except:
            raise BadRequest(
                "The goal was not found or was already marked as achieved")

        goal.set_achieved()
        return send_response(None, 'This goal has been marked as achieved')
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        try:
            goal = Goal.objects.get(id=pk, achieved=False)
        except:
            raise BadRequest(
                "The goal was not found or was already marked as achieved")

        goal.set_canceled()
        return send_response(None, 'This goal has been marked as canceled')


class GaolListView(generics.ListAPIView):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()
    pagination_class = StandardResultsSetPagination
