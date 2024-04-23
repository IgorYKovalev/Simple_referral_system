import time
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomUserSerializer
from app_referral.serializers import ReferralUserSerializer
from .models import CustomUser
from .utils import generate_invite_code
from app_referral.models import ReferralUser


class RegisterUserAPIView(APIView):
    """
    Register a user with a phone number.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        description='Register user with phone number.',
        request=CustomUserSerializer,
        responses={
            201: CustomUserSerializer(),
            400: CustomUserSerializer(),
            500: CustomUserSerializer(),
        }
    )
    def post(self, request):
        """
        Register user with phone number.

        Parameters:
        - phone_number (str): User phone number.

        Returns:
        - Response: HTTP response.
        """
        phone_number = request.data.get('phone_number', None)
        try:
            if phone_number:
                user, created = CustomUser.objects.get_or_create(phone_number=phone_number)
                if created:
                    user.invite_code = generate_invite_code()
                    user.save()
                    # Имитация задержки в 2 секунды
                    time.sleep(2)
                return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Phone number is required.'})


class VerifyUserAPIView(APIView):
    """
    Verify user using phone number and verification code.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        description='Verify user using phone number and verification code.',
        request=CustomUserSerializer,
        responses=CustomUserSerializer,
    )
    def post(self, request):
        """
        Verify user using phone number and verification code.

        Parameters:
        - phone_number (str): User phone number.
        - verification_code (str): Verification code sent to the user.

        Returns:
        - Response: HTTP response.
        """
        phone_number = request.data.get('phone_number', None)
        verification_code = request.data.get('verification_code', None)
        try:
            if phone_number and verification_code:
                user = CustomUser.objects.filter(phone_number=phone_number).first()
                if user and user.password_phone == verification_code:
                    return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Invalid phone number or verification code.'})


class UserProfileAPIView(APIView):
    """
    Get user profile.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description='Get user profile.',
        request=CustomUserSerializer,
        responses={
            200: CustomUserSerializer(),
            500: CustomUserSerializer(),
        }
    )
    def get(self, request):
        """
        Get user profile.

        Returns:
        - Response: User profile.
        """
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        description='Update user profile.',
        request=CustomUserSerializer,
        responses={
            200: CustomUserSerializer(),
            400: CustomUserSerializer(),
            500: CustomUserSerializer(),
        }
    )
    def patch(self, request):
        """
        Update user profile.

        Parameters:
        - invite_code (str, optional): Invite code to activate.

        Returns:
        - Response: HTTP response.
        """
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            invite_code = serializer.validated_data.get('invite_code')
            if invite_code:
                referrer_user = CustomUser.objects.filter(invite_code=invite_code).first()
                if referrer_user and referrer_user != user:
                    if ReferralUser.objects.filter(i_invited=user).exists():
                        return Response(
                            data={'error': 'User has already activated an invite code.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    ReferralUser.objects.create(i_invited=user, he_invited_me=referrer_user)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateInviteCodeAPIView(APIView):
    """
    Activate invite code.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description='Activate invite code.',
        request=CustomUserSerializer,
        responses={
            200: CustomUserSerializer(many=False),
            400: CustomUserSerializer(),
            500: CustomUserSerializer(),
        }
    )
    def post(self, request):
        """
        Activate invite code.

        Parameters:
        - invite_code (str): Invite code to activate.

        Returns:
        - Response: HTTP response.
        """
        invite_code = request.data.get('invite_code', None)
        try:
            if invite_code:
                referrer_user = CustomUser.objects.filter(invite_code=invite_code).first()
                if referrer_user and referrer_user != request.user:
                    ReferralUser.objects.get_or_create(i_invited=request.user, he_invited_me=referrer_user)
                    return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Invalid invite code.'})


class InvitedUsersAPIView(APIView):
    """
    Get users invited by the current user.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description='Get users invited by the current user.',
        request=CustomUserSerializer,
        responses={
            200: ReferralUserSerializer(many=True),
            500: CustomUserSerializer(),
        }
    )
    def get(self, request):
        """
        Get users invited by the current user.

        Returns:
        - Response: List of invited users.
        """
        invited_users = ReferralUser.objects.filter(i_invited=request.user)
        serializer = ReferralUserSerializer(invited_users, many=True)
        return Response(serializer.data)
