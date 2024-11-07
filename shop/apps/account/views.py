from django.contrib.auth import authenticate, login
from rest_framework import status, generics, permissions
from rest_framework.response import Response
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




class RegisterUserView(generics.CreateAPIView):
    """View for registering a new CustomUser."""
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        random_number = funcs.create_random_code(5)
        try:
            user = CustomUser.objects.get(mobile_number=request.data.get('mobile_number'))
            user.set_password(request.data.get('password'))
            user.active_code = random_number
            user.save()

            # Store essential info in session
            request.session['user_info'] = {
                'mobile_number': user.mobile_number,
                'active_code': random_number,
                'remember_password': False,
            }
            return response
        except CustomUser.DoesNotExist:
            return Response({'message': 'Registration failed. User not found.'}, status=status.HTTP_404_NOT_FOUND)


class RegisterActiveCode(generics.CreateAPIView):
    """View for activating a registered user with a code."""
    queryset = CustomUser.objects.all()
    serializer_class = ActiveCodeSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
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


class LoginUserGeneric(generics.CreateAPIView):
    """View for authenticating and logging in a CustomUser."""
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
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


class RememberPasswordGeneric(generics.CreateAPIView):
    """View for handling password reset by sending an active code."""
    queryset = CustomUser.objects.all()
    serializer_class = RememberPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
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


class ChangePasswordGeneric(generics.CreateAPIView):
    """View for changing a CustomUser's password."""
    queryset = CustomUser.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        password = request.data.get('password')
        re_password = request.data.get('re_password')

        if password == re_password:
            user_info = request.session.get('user_info', {})
            user = get_object_or_404(CustomUser, mobile_number=user_info.get('mobile_number'))

            user.set_password(password)
            user.save()
            return Response({'message': 'Password changed successfully.'})
        return Response({'message': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
