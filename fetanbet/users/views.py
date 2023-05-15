from .serializers import UserSerializer, SignUpSerializer, LoginSerializer
from rest_framework import permissions,viewsets,views,permissions,status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from datetime import datetime,timedelta
from .utils import load_token
from knox.views import LoginView as knoxLoginView
from knox.models import AuthToken



# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class SignUp(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(status=status.HTTP_200_OK, data='email confirmation sent')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmail(views.APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, token):
        user_id, timestamp=load_token(token)
        if datetime.now()-datetime.fromisoformat(timestamp) > timedelta(days=1):
            return Response(status=status.HTTP_400_BAD_REQUEST, data="time limit exeeds")
        try:
            user = get_user_model().objects.get(id=user_id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="the token is not correct")
        
        user.is_active=True
        user.save()
        return Response(status=status.HTTP_200_OK, data='email confirmed')


class LoginView(knoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user and user.is_active:
            return Response(status=status.HTTP_200_OK, data = AuthToken.objects.create(user = user)[1])
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="password or email incorrect")