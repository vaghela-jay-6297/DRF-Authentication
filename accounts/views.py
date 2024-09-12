from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from Reg_Log_JWT_DRF.permissions import UpdateOnlyPermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer, LoginSerializer, ChangePasswordSerializer


class RegisterAPIView(generics.CreateAPIView):
    """ API endpoint for user registration with role selection (admin or employee). """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]


class LoginAPIView(APIView):
    """ API endpoint for login using username or email and password. Returns JWT token on successful login. """
    permission_classes = [AllowAny, ]  # all user perform login
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User logged in successfully',
            'Access Token': str(refresh.access_token),
            'Refresh Token': str(refresh),
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'authenticatedUser': {
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        })


class MyProfileAPIView(generics.RetrieveAPIView):
    """ API endpoint for getting logged-in user info - requires JWT authentication. """
    permission_classes = [IsAuthenticated, ]

    # override method
    def retrieve(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response({
            'message': 'Successfully fetched logged-in User Info.',
            'success': True,
            'status_code': status.HTTP_200_OK,
            'User_Info': {
                'username': serializer.data['username'],
                'email': serializer.data['email'],
                'role': serializer.data['role'],
                'created_at': request.user.created_at,
                'updated_at': request.user.updated_at
            }
        })


class UserViewSet(viewsets.ModelViewSet):
    """ API endpoint for logged-in user profile management (list, retrieve, update, delete) - requires JWT
    authentication."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UpdateOnlyPermission ]  # user must authenticate & users have only update permissions


class ChangePasswordAPIView(generics.UpdateAPIView):
    """ API endpoint for logged-in user Change their password """
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated, ]

    # override method
    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])    # set new password
            user.save()

            # serialize requested user's data
            serializer = UserSerializer(request.user)
            return Response({
                'message': 'Password Successfully Changed.',
                'success': True,
                'status_code': status.HTTP_200_OK,
                'User_Info': {
                    'username': serializer.data['username'],
                    'email': serializer.data['email'],
                    'role': serializer.data['role'],
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)