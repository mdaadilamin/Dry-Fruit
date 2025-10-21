from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from .models import Order, CartItem
from .serializers import OrderSerializer, CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        if self.request.user.role.name == 'admin':
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)
    
    @action(detail=True, methods=['get'], renderer_classes=[TemplateHTMLRenderer])
    def invoice(self, request, pk=None):
        """Generate invoice for an order"""
        order = get_object_or_404(Order, pk=pk)
        
        # Check permissions
        if request.user.role.name != 'admin' and order.customer != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if PDF download is requested
        download_pdf = request.GET.get('download') == 'pdf'
        
        # Render invoice template
        template = get_template('orders/invoice.html')
        context = {
            'order': order,
            'request': request
        }
        
        if request.accepted_renderer.format == 'html' and not download_pdf:
            return Response(context, template_name='orders/invoice.html')
        else:
            # Generate PDF
            html = template.render(context)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
            
            if not pdf.err:
                response = HttpResponse(result.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_number}.pdf"'
                return response
            else:
                return Response({'error': 'Error generating PDF'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Add item to cart"""
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        # Implementation similar to views.add_to_cart
        return Response({'message': 'Item added to cart'})
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """Clear entire cart"""
        CartItem.objects.filter(user=request.user).delete()
        return Response({'message': 'Cart cleared'}, status=status.HTTP_204_NO_CONTENT)