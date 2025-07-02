from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import HasKeycloakRole

class AdminOnlyPermission(HasKeycloakRole):
    required_role = "admin"

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hello_view(request):
    print(f'request.auth: {request.auth}')
    user = request.user
    return Response({
        "message": f"Olá, {user.username}! Teste de autenticação"
    })

class AdminOnlyHelloView(APIView):
    permission_classes = [IsAuthenticated, AdminOnlyPermission]
    
    def get(self, request):
        print(f'request.auth: {request.auth}')
        return Response({"message": f"Olá {request.user}, você tem a role admin!"})