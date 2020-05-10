from rest_framework import serializers

from payment.models import LipaOnline,PayBill,EasyPay, CardPayment


class LipaOnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipaOnline
        fields = ("id","mobileNumber","amount",)
        
class PayBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayBill
        fields = ("id","mobileNumber","amount",)
        
class EasyPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = EasyPay
        fields = ("id","mobileNumber","amount",)

class CardPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardPayment
        fields = ("id", "mobileNumber", "amount", "cardNumber",)