import requests
from jose import jwt, jwk
from jose.utils import base64url_decode
from jose.exceptions import JWTError
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

class KeycloakJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ")[1]
        jwks_url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
        try:
            jwks = requests.get(jwks_url).json()
            for key in jwks['keys']:
                try:
                    payload = jwt.decode(
                        token,
                        key,
                        algorithms=['RS256'],
                        audience=settings.KEYCLOAK_CLIENT_ID,
                        issuer=settings.KEYCLOAK_ISSUER
                    )
                    return (AnonymousUser(), payload)
                except JWTError as e:
                    print(f'Token inválido com essa chave: {e}')
                    continue

        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Erro ao buscar JWKS: {str(e)}")

        raise exceptions.AuthenticationFailed("Token inválido.")
