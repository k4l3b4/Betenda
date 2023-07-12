# Create your views here.
# from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from Betenda.methods import BadRequest, PermissionDenied, ResourceNotFound, check_user_permissions, send_response
from .models import Poem, Saying, Sentence, Language, Word
from .serializers import PoemSerializer, SayingSerializer, SentenceSerializer, LanguageSerializer, WordSerializer


class Language_CUD_APIView(APIView):
    # setting level authentication class set so no need to set here
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        groups = ['Admin']
        perms = ['Contributions.add_language']
        print(user.get_all_permissions())
        if check_user_permissions(user=user, groups=groups, perms=perms):
            serializer = LanguageSerializer(data=request.data)
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response(serializer.data, "Language registered successfully", 201)
        raise PermissionDenied("You don't have permission for this action")

    def patch(self, request, *args, **kwargs):

        try:
            id = request.data['id']
        except:
            raise BadRequest(
                "Needed information was not included: resource ID")

        user = request.user
        groups = ['Admin']
        perms = ['Contributions.change_language']
        try:
            instance = Language.objects.get(id=id)
        except:
            raise ResourceNotFound("The language was not found")

        if check_user_permissions(user=user, groups=groups, perms=perms):
            serializer = LanguageSerializer(instance=instance,
                                            data=request.data, partial=True)
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response(serializer.data, "Language updated successfully")
        raise PermissionDenied("You don't have permission for this action")

    def delete(self, request, *args, **kwargs):

        try:
            id = request.data['id']
        except:
            raise BadRequest(
                "Needed information was not included: resource ID")

        user = request.user
        groups = ['Admin']
        perms = ['Contributions.delete_language']
        try:
            instance = Language.objects.get(id=id)
        except:
            raise ResourceNotFound("The language was not found")

        if check_user_permissions(user=user, groups=groups, perms=perms):
            instance.delete()
            return send_response(None, "Language deleted successfully")
        raise PermissionDenied("You don't have permission for this action")


class Word_CUD_APIView(APIView):
    # setting level authentication class set so no need to set here
    queryset = Word.objects.all()
    serializer_class = WordSerializer

    def post(self, request, *args, **kwargs):
        user = request.user

        serializer = WordSerializer(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)
        serializer.save(user=user)
        return send_response(serializer.data, "Word added successfully", 201)

    def patch(self, request, *args, **kwargs):
        user = request.user
        try:
            id = request.data['id']
        except:
            raise BadRequest(
                "Needed information was not included: resource ID")

        try:
            instance = Word.objects.get(id=id)
        except:
            raise ResourceNotFound()
        
        if user.id != instance.user_id:
            raise PermissionDenied("You are not allowed to update this word")

        serializer = WordSerializer(instance=instance,
                                    data=request.data, partial=True)
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)
        serializer.save()
        return send_response(serializer.data, "Word updated successfully")


class Poem_CUD_APIView(APIView):
    # setting level authentication class set so no need to set here
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer

    def post(self, request, *args, **kwargs):
        user = request.user

        serializer = PoemSerializer(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)
        serializer.save(user=user)
        return send_response(serializer.data, "Poem added successfully", 201)

    def patch(self, request, *args, **kwargs):
        user = request.user

        try:
            id = request.data['id']
        except:
            raise BadRequest(
                "Needed information was not included: resource ID")

        try:
            instance = Poem.objects.get(id=id)
        except:
            raise ResourceNotFound("Poem was not found")

        if user.id != instance.user_id:
            raise PermissionDenied("You are not allowed to update this word")
        
        serializer = PoemSerializer(instance=instance,
                                    data=request.data, partial=True)
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)
        serializer.save()
        return send_response(serializer.data, "Poem updated successfully")


class Saying_CUD_APIView(APIView):
    # setting level authentication class set so no need to set here
    queryset = Saying.objects.all()
    serializer_class = SayingSerializer

    def post(self, request, *args, **kwargs):
        user = request.user

        serializer = SayingSerializer(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)
        serializer.save(user=user)
        return send_response(serializer.data, "Saying added successfully", 201)

    def patch(self, request, *args, **kwargs):
        user = request.user
        try:
            id = request.data['id']
        except:
            raise BadRequest(
                "Needed information was not included: resource ID")

        try:
            instance = Saying.objects.get(id=id)
        except:
            raise ResourceNotFound("Saying was not found")

        if user.id != instance.user_id:
            raise PermissionDenied("You are not allowed to update this saying")

        serializer = SayingSerializer(instance=instance,
                                      data=request.data, partial=True)
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)
        serializer.save()
        return send_response(serializer.data, "Saying updated successfully")


class Sentence_CUD_APIView(APIView):
    # setting level authentication class set so no need to set here
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer

    def post(self, request, *args, **kwargs):
        user = request.user

        serializer = SentenceSerializer(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)
        serializer.save(user=user)
        return send_response(serializer.data, "Sentence added successfully", 201)

    def patch(self, request, *args, **kwargs):
        user = request.user
        try:
            id = request.data['id']
        except:
            raise BadRequest(
                "Needed information was not included: resource ID")

        try:
            instance = Sentence.objects.get(id=id)
        except:
            raise ResourceNotFound("Sentence was not found")

        if user.id != instance.user_id:
            raise PermissionDenied("You are not allowed to update this sentence")

        serializer = SentenceSerializer(instance=instance,
                                        data=request.data, partial=True)
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)
        serializer.save()
        return send_response(serializer.data, "Sentence updated successfully")
