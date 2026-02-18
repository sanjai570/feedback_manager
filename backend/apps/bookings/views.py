from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.common.permissions import IsAdmin, IsStaffOrAdmin, IsStudent, IsOwnerOrAdmin
from .services import BookingService
from .serializers import BookingSerializer
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Booking

class BookingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # "Enforce Query Filtering (Students see own bookings only)"
        if request.user.role == 'STUDENT':
            bookings = Booking.objects.filter(user=request.user)
        else:
            # Staff/Admin see all
            bookings = BookingService.get_all_bookings()
        
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Student creates booking
        # Staff/Admin can too potentially
        
        # Service handles validation and double booking check
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            data['user'] = request.user
            
            # Enforce PENDING status for everyone initially? 
            # Or allow Admin/Staff to set APPROVED?
            # "Status defaults to PENDING".
            # Let's rely on service.
            
            try:
                booking = BookingService.create_booking(data)
                return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                # Handle django.core.exceptions.ValidationError
                if hasattr(e, 'message_dict'):
                     return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
                return Response({"non_field_errors": [str(e.message)]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        booking = get_object_or_404(Booking, id=pk)
        
        # Student: View ONLY own bookings
        if request.user.role == 'STUDENT' and booking.user != request.user:
             return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
             
        return Response(BookingSerializer(booking).data)

    def put(self, request, pk):
        booking = get_object_or_404(Booking, id=pk)
        
        # "Students CANNOT change status."
        # "STAFF: ... Approve / Reject bookings"
        
        if request.user.role == 'STUDENT':
             return Response({'error': 'Permission denied: Students cannot update bookings'}, status=status.HTTP_403_FORBIDDEN)

        # Only Staff/Admin can update (Validation logic for status)
        if request.user.role not in ['ADMIN', 'STAFF']:
             return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        serializer = BookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
             try:
                 # If status is changing, Service likely handles it, or we save here.
                 # Let's ensure update_booking_status is used if status is present? 
                 # Or just save serializer.
                 serializer.save()
                 return Response(serializer.data)
             except Exception as e:
                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        booking = get_object_or_404(Booking, id=pk)
        
        # "ADMIN: Full booking control" -> Can delete
        # "STAFF: Approve/Reject" -> No delete mentioned vs "User module: Read-only". 
        # But "Resources: Create+Update".
        # Usually Cancel is a status update to 'CANCELLED'. 
        # Delete suggests hard delete. Let's restrict to ADMIN.
        
        if request.user.role != 'ADMIN':
            return Response({'error': 'Permission denied: Only Admin can delete bookings'}, status=status.HTTP_403_FORBIDDEN)
            
        BookingService.delete_booking(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        return self.put(request, pk)
