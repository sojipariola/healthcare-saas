"""
Authentication ViewSets for JWT tokens
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with additional claims"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['role'] = str(user.role) if user.role else 'user'
        token['tenant_id'] = str(user.tenant_id) if hasattr(user, 'tenant_id') else None
        
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token obtain view"""
    serializer_class = CustomTokenObtainPairSerializer


class AuthViewSet(viewsets.ViewSet):
    """
    Authentication endpoints
    - Login (get JWT tokens)
    - Refresh token
    - Get current user
    - Logout (blacklist token)
    """
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current authenticated user info"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Logout user (can blacklist token if using token blacklist package)"""
        return Response(
            {'status': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a new user"""
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        
        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'User with this email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        serializer = UserSerializer(user)
        return Response(
            {'user': serializer.data, 'message': 'User registered successfully'},
            status=status.HTTP_201_CREATED
        )
