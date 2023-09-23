from rest_framework.permissions import BasePermission, exceptions
from django.conf import settings
import jwt

class CustomPermision(BasePermission):

  def has_permission(self, request, view):

        token = request.COOKIES.get('jwt')
        token_is_verified = False

        try:
          payload = jwt.decode(token, settings.JWT_KEY, algorithms=['HS256'])
          token_is_verified = True

        except:
          raise exceptions.AuthenticationFailed('Unauthorized')

        return bool(request.user and token_is_verified)