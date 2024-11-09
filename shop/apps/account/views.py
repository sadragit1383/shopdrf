from django.contrib.auth import authenticate, login
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
import funcs  # pylint: disable=import-error
from .models import CustomUser
from .serializers import (
    CustomUserSerializer,
    RegisterSerializer,
    LoginSerializer,
    RememberPasswordSerializer,
    ChangePasswordSerializer,
    ActiveCodeSerializer
)



class CustomerUserView(generics.ListCreateAPIView):
    """View for listing and creating CustomUser instances."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]  # Use JWT authentication

class CustomUserViewDetail(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting CustomUser instances."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # Use JWT authentication


class RegisterUserView(APIView):
    """View for registering a new CustomUser."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            random_number = funcs.create_random_code(5)
            user = CustomUser.objects.get(mobile_number=request.data.get('mobile_number'))
            user.set_password(request.data.get('password'))
            user.active_code = random_number
            user.save()

            request.session['user_info'] = {
                'mobile_number': user.mobile_number,
                'active_code': random_number,
                'remember_password': False,
            }
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterActiveCode(APIView):
    """View for activating a registered user with a code."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_info = request.session.get('user_info', {})
        mobile_number = user_info.get('mobile_number')
        active_code = user_info.get('active_code')

        user = get_object_or_404(CustomUser, mobile_number=mobile_number)
        if int(active_code) == int(request.data.get('active_code')):
            if not user_info.get('remember_password'):
                user.is_active = True
                user.save()
                return Response({'message': 'User successfully activated.'})
            return Response({'message': 'Password reset successful.'})
        return Response({'message': 'Incorrect code entered.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginUserGeneric(APIView):
    """View for authenticating and logging in a CustomUser."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        mobile_number = request.data.get('mobile_number')
        password = request.data.get('password')
        user = authenticate(request, username=mobile_number, password=password)

        if user:
            if user.is_active:
                if not user.is_admin:
                    login(request, user)
                    return Response({'message': 'Login successful.'})
                return Response({'message': 'Admin users cannot log in here.'}, status=status.HTTP_403_FORBIDDEN)
            return Response({'message': 'User is not active.'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)


class RememberPasswordGeneric(APIView):
    """View for handling password reset by sending an active code."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        mobile_number = request.data.get('mobile_number')
        user = get_object_or_404(CustomUser, mobile_number=mobile_number)

        random_number = funcs.create_random_code(5)
        user.active_code = random_number
        user.save()

        request.session['user_info'] = {
            'mobile_number': user.mobile_number,
            'active_code': random_number,
            'remember_password': True
        }

        return Response({'message': 'Code sent successfully.'})


class ChangePasswordGeneric(APIView):
    """View for changing a CustomUser's password."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        password = request.data.get('password')
        re_password = request.data.get('re_password')

        if password == re_password:
            user_info = request.session.get('user_info', {})
            user = get_object_or_404(CustomUser, mobile_number=user_info.get('mobile_number'))

            user.set_password(password)
            user.save()
            return Response({'message': 'Password changed successfully.'})
        return Response({'message': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
