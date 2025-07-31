from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, UserSerializer

# Login API
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'detail': 'Logged in successfully.'}, status=status.HTTP_200_OK)
    return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

# Register API
@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'detail': 'User created successfully.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Profile Update API
@api_view(['POST'])
def profile_update(request):
    if request.user.is_authenticated:
        user = request.user
        user.username = request.data.get('username', user.username)
        user.first_name = request.data.get('firstname', user.first_name)
        user.last_name = request.data.get('lastname', user.last_name)
        user.email = request.data.get('email', user.email)
        user.save()
        return Response({'detail': 'Profile updated successfully.'}, status=status.HTTP_200_OK)
    return Response({'detail': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

# Create Post API
@api_view(['POST'])
def create_post(request):
    if request.user.is_authenticated:
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

# Add Comment API
@api_view(['POST'])
def add_comment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.user.is_authenticated:
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, name=request.user.username, email=request.user.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

# Logout API
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)

# CSRF Token API
@api_view(['GET'])
@ensure_csrf_cookie
def get_csrf_token(request):
    return Response({'detail': 'CSRF cookie set'})
