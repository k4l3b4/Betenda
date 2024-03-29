from betenda_api.pagination import StandardResultsSetPagination
from rest_framework import generics
from rest_framework.views import APIView
from betenda_api.methods import BadRequest, PermissionDenied, ResourceNotFound, ServerError, check_user_permissions, send_response, validate_key_value
from .models import Poem, Saying, Sentence, Language, Word
from .serializers import Poem_LCU_Serializer, SayingSerializer, SentenceSerializer, LanguageSerializer, WordSerializer


class Language_CUD_APIView(APIView):
    # setting level authentication class set so no need to set here
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    def get(self, request, *args, **kwargs):
        try:
            instance = self.queryset.all()
            serializer = self.serializer_class(instance, many=True)
            return send_response(serializer.data, "Languages retrieved successfully")
        except:
          return ServerError("There was an error on our side")


    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            groups = ['Admin']
            perms = ['Contributions.add_language']
            if check_user_permissions(user=user, groups=groups, perms=perms):
                serializer = self.serializer_class(data=request.data)
                if not serializer.is_valid():
                    raise BadRequest(serializer.errors)
                serializer.save()
                return send_response(serializer.data, "Language registered successfully", 201)
            raise PermissionDenied("You don't have permission for this action")
        except:
          raise ServerError("There was an error on our side")


    def patch(self, request, *args, **kwargs):
        try:
            id = request.data.get('id')

            if not id:
                raise BadRequest("Needed information was not included: resource ID")

            user = request.user
            groups = ['Admin']
            perms = ['Contributions.change_language']
            try:
                instance = self.queryset.get(id=id)
            except:
                raise ResourceNotFound("The language was not found")

            if check_user_permissions(user=user, groups=groups, perms=perms):
                serializer = self.serializer_class(instance=instance,
                                                data=request.data, partial=True)
                if not serializer.is_valid():
                    raise BadRequest(serializer.errors)
                serializer.save()
                return send_response(serializer.data, "Language updated successfully")
            raise PermissionDenied("You don't have permission for this action")
        except:
          return ServerError("There was an error on our side")

    def delete(self, request, *args, **kwargs):
        try:
            id = request.GET.get('id')
            # rases exception if key isn't present or is empty ""
            validate_key_value(id, "ID")

            user = request.user
            groups = ['Admin']
            perms = ['Contributions.delete_language']
            try:
                instance = self.queryset.get(id=id)
            except:
                raise ResourceNotFound("The language was not found")

            if check_user_permissions(user=user, groups=groups, perms=perms):
                instance.delete()
                return send_response(None, "Language deleted successfully")
            raise PermissionDenied("You don't have permission for this action")
        except:
          return ServerError("There was an error on our side")



class Word_CU_APIView(APIView):
    # setting level authentication class set so no need to set here
    queryset = Word.objects.all()
    serializer_class = WordSerializer

    def post(self, request, *args, **kwargs):
        try:
            perms = ['Contributions.add_word']
            user = request.user
            mutable_data = request.data.copy()
            # if mutable_data['synonym']:
            #     mutable_data['synonym'] = [int(x) if x else None for x in mutable_data['synonym'] if x.strip()]
            # if mutable_data['antonym']:
            #     mutable_data['antonym'] = [int(x) if x else None for x in mutable_data['antonym'] if x.strip()]
            if check_user_permissions(user=user, groups=None, perms=perms):
                serializer = self.serializer_class(data=mutable_data)
                if not serializer.is_valid():
                    raise BadRequest(serializer.errors)
                serializer.save(user=user)
                return send_response("Word added successfully", 201)
            raise PermissionDenied("You don't have permission for this action")
        except:
          raise ServerError("There was an error on our side")


    def patch(self, request, *args, **kwargs):
        try:
            user = request.user
            try:
                id = request.data['id']
            except:
                raise BadRequest(
                    "Needed information was not included: resource ID")

            try:
                instance = self.queryset.get(id=id)
            except:
                raise ResourceNotFound()

            if user.id != instance.user_id:
                raise PermissionDenied("You are not allowed to update this word")

            serializer = self.serializer_class(instance=instance,
                                        data=request.data, partial=True)
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response("Word updated successfully")
        except:
          return ServerError("There was an error on our side")


class Poem_GCU_APIView(APIView):
    # setting level authentication class set so no need to set here
    queryset = Poem.objects.all()
    serializer_class = Poem_LCU_Serializer

    def get(self, request, slug, *args, **kwargs):
        if not slug:
            raise BadRequest("Needed information was not included: slug")
        
        try:
          poem = self.queryset.get(slug=slug)
        except:
          raise ResourceNotFound("The poem was not found")
        
        serializer = self.serializer_class(poem)
        return send_response(serializer.data, "Poem retrieved successfully", 200)

    def post(self, request, *args, **kwargs):
        # try:
            perms = ['Contributions.add_poem']
            user = request.user

            if check_user_permissions(user=user, groups=None, perms=perms):
                serializer = self.serializer_class(data=request.data)
                if not serializer.is_valid():
                    raise BadRequest(serializer.errors)
                serializer.save(user=user)
                return send_response("Poem added successfully", 201)
            raise PermissionDenied("You don't have permission for this action")
        # except:
        #   return ServerError("There was an error on our side")

    def patch(self, request, *args, **kwargs):
        try:
            user = request.user

            try:
                id = request.data['id']
            except:
                raise BadRequest(
                    "Needed information was not included: resource ID")

            try:
                instance = self.queryset.get(id=id)
            except:
                raise ResourceNotFound("Poem was not found")

            if user.id != instance.user_id:
                raise PermissionDenied("You are not allowed to update this poem")

            serializer = self.serializer_class(instance=instance,
                                        data=request.data, partial=True)
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response("Poem updated successfully")
        except:
          return ServerError("There was an error on our side")
      


class Saying_CU_APIView(APIView):
    # setting level authentication class set so no need to set here
    queryset = Saying.objects.all()
    serializer_class = SayingSerializer

    def post(self, request, *args, **kwargs):
        try:
            perms = ['Contributions.add_saying']
            user = request.user

            if check_user_permissions(user=user, groups=None, perms=perms):
                serializer = self.serializer_class(data=request.data)
                if not serializer.is_valid():
                    raise BadRequest(serializer.errors)
                serializer.save(user=user)
                return send_response("Saying added successfully", 201)
            raise PermissionDenied("You don't have permission for this action")
        except:
          return ServerError("There was an error on our side")


    def patch(self, request, *args, **kwargs):
        try:
            user = request.user
            try:
                id = request.data['id']
            except:
                raise BadRequest(
                    "Needed information was not included: resource ID")

            try:
                instance = self.queryset.get(id=id)
            except:
                raise ResourceNotFound("Saying was not found")

            if user.id != instance.user_id:
                raise PermissionDenied("You are not allowed to update this saying")

            serializer = self.serializer_class(instance=instance,
                                        data=request.data, partial=True)
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response(serializer.data, "Saying updated successfully")
        except:
          return ServerError("There was an error on our side")



class Sentence_CU_APIView(APIView):
    # setting level authentication class set so no need to set here
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer

    def post(self, request, *args, **kwargs):
        try:
            perms = ['Contributions.add_sentence']
            user = request.user
            if check_user_permissions(user=user, groups=None, perms=perms):
                serializer = self.serializer_class(data=request.data)
                if not serializer.is_valid():
                    raise BadRequest(serializer.errors)
                serializer.save(user=user)
                return send_response(serializer.data, "Sentence added successfully", 201)
            raise PermissionDenied("You don't have permission for this action")
        except:
          return ServerError("There was an error on our side")


    def patch(self, request, *args, **kwargs):
        try:
            user = request.user
            try:
                id = request.data['id']
            except:
                raise BadRequest(
                    "Needed information was not included: resource ID")

            try:
                instance = self.queryset.get(id=id)
            except:
                raise ResourceNotFound("Sentence was not found")

            if user.id != instance.user_id:
                raise PermissionDenied(
                    "You are not allowed to update this sentence")

            serializer = self.serializer_class(instance=instance,
                                            data=request.data, partial=True)
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response(serializer.data, "Sentence updated successfully")
        except:
          return ServerError("There was an error on our side")


class Poem_List_APIView(generics.ListAPIView):
    queryset = Poem.objects.all()
    serializer_class = Poem_LCU_Serializer
    pagination_class = StandardResultsSetPagination