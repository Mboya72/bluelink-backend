from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import MpesaService
from .models import Transaction, Escrow, Wallet
from orders.models import Order

class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        phone = request.data.get('phone') # Format: 2547XXXXXXXX
        order = Order.objects.get(id=order_id)
        
        response = MpesaService.stk_push(phone, order.total_amount, order_id)
        return Response(response)

class MpesaCallbackView(APIView):
    """Safaricom sends data here after the user enters their PIN."""
    def post(self, request):
        data = request.data.get('Body').get('stkCallback')
        result_code = data.get('ResultCode')
        
        if result_code == 0:  # Success
            metadata = data.get('CallbackMetadata').get('Item')
            amount = next(item for item in metadata if item["Name"] == "Amount")["Value"]
            receipt = next(item for item in metadata if item["Name"] == "MpesaReceiptNumber")["Value"]
            order_ref = data.get('CheckoutRequestID') # Use this to map to your Escrow

            # Logic: 1. Create Transaction, 2. Update Escrow to 'HELD'
            # Note: You'll need to save the CheckoutRequestID in your Escrow model earlier.
            print(f"Payment Successful: {receipt}, Amount: {amount}")
            
        return Response({"ResultCode": 0, "ResultDesc": "Accepted"})