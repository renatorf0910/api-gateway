from rest_framework_simplejwt.authentication import JWTAuthentication
from jose import jwt
from jose.exceptions import JWTError
from django.conf import settings
import requests

class KeycloakJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        jwks_url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
        jwks = requests.get(jwks_url).json()
        for key in jwks["keys"]:
            try:
                return jwt.decode(
                    raw_token,
                    key=key,
                    algorithms=["RS256"],
                    audience=settings.KEYCLOAK_CLIENT_ID,
                )
            except JWTError:
                continue
        raise Exception("Token inválido ou não assinado corretamente")
