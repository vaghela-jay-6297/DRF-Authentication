from django.shortcuts import render
from .models import Tool
from .serializers import ToolSerializer
from rest_framework import generics
from Reg_Log_JWT_DRF.permissions import IsAuthenticatedAdminUser
from rest_framework.permissions import IsAuthenticated


class ToolListCreateView(generics.ListCreateAPIView):
    """API Endpoint for Retrieve tool list & create toos but Only Admin User can create tool."""
    queryset = Tool.objects.filter(active=True)
    serializer_class = ToolSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """if request is post than required admin user only to create/post tool"""
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticatedAdminUser, ]
        return super().get_permissions()


class ToolRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """API Endpoint for get tool details, update & delete tool but Only Admin User can update & delete tool."""
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  # we can also pass another field of model field like name, active, description

    def get_permissions(self):
        """if request is 'PUT', 'PATCH', 'DELETE' than required admin user only to update & delete tool"""
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticatedAdminUser]
        return super().get_permissions()
