from rest_framework import status, views, generics, permissions, authentication
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from .models import Purchase, Voucher, Ecommerce, PurchaseVoucher
from .serializers import PurchaseSerializer, LoginSerializer

class ProcessPaymentView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        api_key = data.get('api_key') or request.headers.get('X-Api-Key')
        
        # Validate Ecommerce
        try:
            ecommerce = Ecommerce.objects.get(api_key=api_key)
        except Ecommerce.DoesNotExist:
            return Response({'error': 'Invalid Ecommerce API Key'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Extract Data
        order_id = data.get('order_id')
        amount = data.get('amount')
        voucher_id = data.get('voucher')
        code = data.get('code')
        
        if not all([order_id, amount, voucher_id, code]):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate Voucher
        try:
            voucher = Voucher.objects.get(identifier=voucher_id, security_code=code, is_active=True)
            # Check logic for discount validation if needed
        except Voucher.DoesNotExist:
            # Create failed purchase record
            Purchase.objects.create(
                ecommerce=ecommerce,
                order_id=order_id,
                amount=amount,
                status='failed',
                voucher_code=voucher_id,
                voucher_secret=code
            )
            return Response({'error': 'Invalid Voucher/Code'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create Successful Purchase
        purchase = Purchase.objects.create(
            ecommerce=ecommerce,
            order_id=order_id,
            amount=amount,
            status='completed',
            voucher_code=voucher_id
        )
        PurchaseVoucher.objects.create(purchase=purchase, voucher=voucher)

        return Response({'status': 'authorized', 'purchase_id': purchase.id}, status=status.HTTP_200_OK)

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user:
                login(request, user)
                return Response({'status': 'logged_in', 'user': user.username})
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PurchaseSerializer
    
    def get_queryset(self):
        return Purchase.objects.all().order_by('-timestamp')

class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'status': 'logged_out'}, status=status.HTTP_200_OK)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CsrfView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'success': 'CSRF cookie set'})
