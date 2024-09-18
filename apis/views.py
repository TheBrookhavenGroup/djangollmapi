from rest_framework.views import APIView, View
from rest_framework.response import Response
from .permissions import HasAPIKey
from .tasks import prove_singleton, api_run
from .models import ApiKey, APIRequest


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
        key = request.headers['Authorization'].split()[1]
        text = request.data['text']
        result = api_run.delay(text)
        output = result.get()
        output = output['output']
        r = Response({'message': output})

        k = ApiKey.objects.get(key=key)
        APIRequest.objects.create(key=k, text=text, output=output)

        return r
