from rest_framework import generics
from .models import Books
from .serializers import BooksSerializer, TokenSerializer, UserSerializer
# from ratelimit.decorators import ratelimit
# from ratelimit.mixins import RatelimitMixin
from rest_framework.throttling import UserRateThrottle

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import permissions

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class ListBooksView(generics.ListAPIView):
    # provides a get method handler
    
    throttle_classes = (UserRateThrottle,)

    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = (permissions.IsAuthenticated,)

class LoginView(generics.CreateAPIView):
    
    """
    POST auth/login
    """
    throttle_classes = (UserRateThrottle,)

    # @ratelimit(key='ip', rate='5/m', method='POST')
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = TokenSerializer

    # @ratelimit(key='ip', rate='5/m', method='POST')
    def post(self, request, *args, **kwargs):
        
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            serializer = TokenSerializer(data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )
            })
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class RegisterUsers(generics.CreateAPIView):
    """
    POST auth/register/
    """
    
    throttle_classes = (UserRateThrottle,)

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    # @ratelimit(key='ip', rate='5/m', method='POST')
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        
        if not username and not password and not email :
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )