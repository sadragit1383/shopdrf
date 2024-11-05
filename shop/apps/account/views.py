"""
Module for managing CustomUser authentication and registration views.
"""

from django.contrib.auth import authenticate, login
from rest_framework import status, generics
from rest_framework.response import Response
import funcs # pylint: disable=import-error
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


class CustomUserUserViewDetail(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting CustomUser instances."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class RegisterUserView(generics.CreateAPIView):
    """View for registering a new CustomUser."""
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        random_number = funcs.create_random_code(5)
        user = CustomUser.objects.get(
            mobile_number=request.data.get('mobile_number')
        )
        user.set_password(request.data.get('password'))
        user.active_code = random_number
        user.save()

        request.session['user_info'] = {
            'mobile_number': request.data.get('mobile_number'),
            'active_code': random_number,
            'remember_password': False,
        }

        return response


class RegisterActiveCode(generics.CreateAPIView):
    """View for activating a registered user with a code."""
    queryset = CustomUser.objects.all()
    serializer_class = ActiveCodeSerializer

    def create(self, request, *args, **kwargs):
        user_info = request.session.get('user_info', {})
        try:
            user = CustomUser.objects.get(mobile_number=user_info.get('mobile_number'))
            active_code = user_info.get('active_code')
            if int(active_code) == int(request.data.get('active_code')):
                if not user_info.get('remember_password'):
                    user.is_active = True
                    user.save()
                    return Response({'message': 'Successfully signed up.'})
                return Response({'message': 'Password change successful.'})
            return Response(
                {'message': 'Incorrect code entered.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except CustomUser.DoesNotExist:  # pylint: disable=no-member
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


class LoginUserGeneric(generics.CreateAPIView):
    """View for authenticating and logging in a CustomUser."""
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        mobile_number = request.data.get('mobile_number')
        password = request.data.get('password')
        user = authenticate(request, username=mobile_number, password=password)

        if user:
            if user.is_active:
                if not user.is_admin:
                    login(request, user)
                    return Response({'message': 'Login successful.'})
                return Response(
                    {'message': 'Admin users cannot log in here.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            return Response(
                {'message': 'User is not active.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return Response(
            {'message': 'Invalid credentials.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class RememberPasswordGeneric(generics.CreateAPIView):
    """View for handling password reset by sending an active code."""
    queryset = CustomUser.objects.all()
    serializer_class = RememberPasswordSerializer

    def create(self, request, *args, **kwargs):
        mobile_number = request.data.get('mobile_number')
        try:
            user = CustomUser.objects.get(mobile_number=mobile_number)
            random_number = funcs.create_random_code(5)
            user.active_code = random_number
            user.save()

            request.session['user_info'] = {
                'mobile_number': user.mobile_number,
                'active_code': user.active_code,
                'remember_password': True
            }

            return Response({'message': 'OK'})
        except CustomUser.DoesNotExist:  # pylint: disable=no-member
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordGeneric(generics.CreateAPIView):
    """View for changing a CustomUser's password."""
    queryset = CustomUser.objects.all()
    serializer_class = ChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        password = request.data.get('password')
        re_password = request.data.get('re_password')

        if password and re_password and password == re_password:
            user_info = request.session.get('user_info', {})
            try:
                user = CustomUser.objects.get(mobile_number=user_info.get('mobile_number'))
                user.set_password(password)
                user.save()
                return Response({'message': 'Password changed successfully.'})
            except CustomUser.DoesNotExist:  # pylint: disable=no-member
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {'message': 'Passwords do not match.'},
            status=status.HTTP_400_BAD_REQUEST)