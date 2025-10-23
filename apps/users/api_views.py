from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Role, Permission, Customer
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer, CustomerSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user info"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='customers')
    def customers_list(self, request):
        """Get all customers"""
        # Get the customer role
        try:
            customer_role = Role.objects.get(name='customer')  # type: ignore
            customers = User.objects.filter(role=customer_role)  # type: ignore
            serializer = self.get_serializer(customers, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response([], status=200)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()  # type: ignore
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'], url_path='with-role')
    def with_role(self, request):
        """Get all customers with their user details"""
        customers = Customer.objects.all()  # type: ignore
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()  # type: ignore
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()  # type: ignore
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]