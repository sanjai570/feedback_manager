from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.common.permissions import IsAdmin, IsStaffOrAdmin, IsStudent
from .services import ResourceService
from .serializers import ResourceSerializer

class ResourceListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # All authenticated users can view resources (Student: Read-only)
        resources = ResourceService.get_all_resources()
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Admin: Full CRUD
        # Staff: Create + Update
        # Student: Read-only
        if request.user.role not in ['ADMIN', 'STAFF']:
             return Response({'error': 'Permission denied: Students cannot create resources'}, status=status.HTTP_403_FORBIDDEN)
             
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            resource = ResourceService.create_resource(serializer.validated_data)
            return Response(ResourceSerializer(resource).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResourceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        from django.shortcuts import get_object_or_404
        from .models import Resource
        # Authenticated users can view details
        resource = get_object_or_404(Resource, pk=pk)
        return Response(ResourceSerializer(resource).data)

    def put(self, request, pk):
        # Admin: Full CRUD
        # Staff: Create + Update
        if request.user.role not in ['ADMIN', 'STAFF']:
             return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ResourceSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            resource = ResourceService.update_resource(pk, serializer.validated_data)
            return Response(ResourceSerializer(resource).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Admin: Full CRUD
        # Staff: Cannot delete
        if request.user.role != 'ADMIN':
             return Response({'error': 'Permission denied: Only Admin can delete resources'}, status=status.HTTP_403_FORBIDDEN)
        
        ResourceService.delete_resource(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
