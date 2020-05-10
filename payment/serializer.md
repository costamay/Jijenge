from rest_framework import serializers

from payment.models import LipaOnline, EazzyPay


class LipaOnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipaOnline
        fields = ("id","mobileNumber","amount",)
        
class EazzyPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = EazzyPay
        fields = ("id","mobileNumber","amount",)