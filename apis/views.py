from rest_framework.views import APIView, View
from rest_framework.response import Response
from django.http import JsonResponse
from .permissions import HasAPIKey
from .tasks import prove_singleton, api_run


class PermissionTestView(APIView):
    permission_classes = (HasAPIKey,)

    def post(self, request):
        return Response({'message': request.data['text']})


class SingletonView(APIView):
    permission_classes = (HasAPIKey,)

    def get(self, request, *args, **kwargs):
        x = int(kwargs['value'])
        result = prove_singleton.delay(x)
        result = result.get()
        msg = f"The result is {result}"
        return Response({'message': msg})


class ApiView(APIView):
    permission_classes = (HasAPIKey,)

    def get(self, request):
        content = {'message': 'Use a post request.'}
        return Response(content)

    def post(self, request):
        text = request.data['text']
        result = api_run.delay(text)
        output = result.get()
        output = output['output']
        return Response({'message': output})
