from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer
from .authentication import generate_access_token, JWTAuthentication
from rest_framework.views import APIView

# Create your views here.

@api_view(['POST'])
def register(request):
    data = request.data 

    if data['password'] != data['confirm_password']:
        raise exceptions.APIException('Password do not match!')
    
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found!')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Incorrect username or pasword ')
    
    response = Response()

    token = generate_access_token(user)
    response.set_cookie(key='jwt', value=token, httponly=True)

    response.data = {
        'token': token
    }

    return response

@api_view(['POST'])
def logout(request):
    response = Response()
    response.delete_cookie(key='jwt')
    response.data = {
        'message': "Successfully logout"
    }

    return response




class AuthenticatedUser(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = UserSerializer(request.user)
        return Response({
            'data':user.data
        })


@api_view(['GET'])
def users(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)
