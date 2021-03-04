from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status, views, permissions
from .serializers import UserSerializer, LoginSerializer, EmailVerificationSerializer, SetNewPasswordSerializer, \
    ResetPasswordEmailRequestSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
import jwt
import redis

import logging
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.conf import settings
from django.shortcuts import HttpResponse
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)
logger = logging.getLogger('django')
# Create your views here.


class RegisterView(GenericAPIView):
    """
               This api is for registration of new user
              @param request: username,email and password
              @return: it will return the registered user with its credentials
    """
    serializer_class = UserSerializer

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            user.is_active = False
            token = jwt.encode({'email': user.email}, settings.SECRET_KEY, algorithm='HS256')

            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
            email_body = 'Hi ' + user.username + \
                         ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}
            Util.send_email(data).delay(10)
            logger.info("Email Sent Successfully to the user")
            return Response(user_data, status=status.HTTP_201_CREATED)

        except jwt.ExpiredSignatureError as identifier:
            logger.error(identifier)
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            logger.error(identifier)
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'error': 'Something Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(views.APIView):
    """
            This api is for verification of email to this application
           @param request: once the account verification link is clicked by user this will take that request
           @return: it will return the response of email activation
     """
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.data.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, ['HS256'])
            user = User.objects.get(email=payload['email'])
            if not user.is_active:
                user.is_active = True
                user.save()
            logger.info("Email Successfully Verified")
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            logger.error(identifier)
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            logger.error(identifier)
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'error': 'Something Went Wrong'}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    """
             This api is used to send reset password request to server
             @param request: user registered email id
             @return: sends a password reset link to user validated email id
    """
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        try:
            user = request.data
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            user_data = serializer.data
            email = request.data.get('email', '')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=user_data['email'])
                token = jwt.encode({'email': user.email}, settings.SECRET_KEY, algorithm='HS256')
                current_site = get_current_site(request).domain
                relativeLink = reverse('password-reset')
                absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
                email_body = 'Hello, \n Use link below to reset your password  \n' + \
                             absurl
                data = {'email_body': email_body, 'to_email': user.email,
                        'email_subject': 'Reset your password'}
                Util.send_email(data)
                logger.info("Email Sent Successfully to the user")
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            logger.error(identifier)
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            logger.error(identifier)
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'error': 'Something went wrong'})


class PasswordTokenCheckAPI(generics.GenericAPIView):
    """
            This api is used to check token sent to reset password
            @param request: token generated for resetting the password
            @return: it will return the response of token validation
    """

    serializer_class = EmailVerificationSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, ['HS256'])
            user = User.objects.get(email=payload['email'])
            if not user:
                return Response({'Password reset verification failed'}, status=status.HTTP_400_BAD_REQUEST)
            logger.info("Email Successfully Verified")
            return Response({'email': 'Successfully Verified'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            logger.error(identifier)
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            logger.error(identifier)
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'error': 'Something went wrong'})


class SetNewPasswordAPIView(generics.GenericAPIView):
    """
            This api is used to set new password
            @param request:new password and token generated for resetting new password
            @return: gives response of password reset
    """

    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response({'success': True, 'message': 'password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(views.APIView):

    def post(self, request):
        # serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # print(request.META.get("HTTP_TOKEN"))
        token = request.META.get("HTTP_TOKEN")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, ['HS256'])
            print(payload)
            user = User.objects.get(id=payload['id'])
            value = redis_instance.get(user.id)
            if not value:
                return Response("Failed to logout", status=status.HTTP_400_BAD_REQUEST)
            else:
                result = redis_instance.delete(user.id)
                if result == 1:
                    return Response("Successully logged out", status=status.HTTP_200_OK)
                else:
                    return Response("Failed to logout please re login", status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError as identifier:
            logger.error(identifier)
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            logger.error(identifier)
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)


class ShowUsersAPIView(views.APIView):
    def get(self, request):
        return HttpResponse(
            list(User.objects.filter(is_active=True).values('username').distinct()),
        )


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user:

            auth_token = jwt.encode(
                {'username': user.username}, settings.SECRET_KEY, algorithm='HS256')

            serializer = UserSerializer(user)

            #data = {'user': serializer.data, 'token': auth_token}

            response = Response({'response': f'You are logged in successfully', 'username': username,'token': auth_token},
                                status=status.HTTP_200_OK)
            response['Authorization'] = auth_token
            #return Response(data, status=status.HTTP_200_OK)
            return response
            # SEND RES
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
