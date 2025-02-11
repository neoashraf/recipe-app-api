from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
# from rest_framework.settings import api_settings
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated


from . import serializers
from . import models
from . import permissions


# Create your views here.

class HelloApiView (APIView):
    
    """Test API view."""

    serializer_class = serializers.HelloSerializer
    
    def get(self, request, format=None):
        """Returns a list of APIView features."""
        
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLs',
        ]
        
        return Response({'message':'Hello Dear', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name."""
        
        serializer = serializers.HelloSerializer(data=request.data)
        
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, rquest, pk=None):
        """Handles updating an object."""
        return Response({'method':'put'})
    
    def patch(self, rquest, pk=None):
        """Patch request, only updates fields provided in the request."""
        return Response({'method':'patch'})
    
    def delete(self, rquest, pk=None):
        """Handles deleting an object."""
        return Response({'method':'delete'})
    
    
class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet."""
    
    serializer_class = serializers.HelloSerializer    
    
    def list(self, request):
        """Returns a hello message."""
        
        a_viewset = [
            'Uses actions (list, create,retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]
        
        return Response({'message': 'Hello', 'a_viewset': a_viewset})
    
    def create(self, request):
        """Create a new hello message"""
        
        serializer = serializers.HelloSerializer(data=request.data)
        
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})
    
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handles creating, updating profiles """
    
    serializer_class = serializers.UserProfileSerializer 
    queryset = models.UserProfile.objects.all()
    
    """ Add authentication and permission class to a viewset"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,) 
    
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')
    
class LoginViewSet(viewsets.ViewSet):
    """ Checks email and password and returns an auth token. """
    
    serializer_class = AuthTokenSerializer
    
    def create(self, request):
        """ Use the ObtainAuthToken APIView to validate and create a token. """
        
        return ObtainAuthToken().post(request)

# class UserLoginApiView(ObtainAuthToken):
#     """Handle creating user authentication tokens"""
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
class ProfileFeedItemViewSet(viewsets.ModelViewSet):
    """ Handles creating, reading and updating profile feed items """
    
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    # permission_classes = (permissions.PostOwnStatus, IsAuthenticatedOrReadOnly)  # anyone can read the data if we use 'IsAuthenticatedOrReadOnly'
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)    # makes profilefeed restricted to only registered users
    
    
    def perform_create(self, serializer):
        """ Sets the user profile to the logged in user. """
        serializer.save(user_profile=self.request.user)