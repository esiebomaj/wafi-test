from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()


class DepositSerializer(serializers.Serializer):
    # this serializer can be used for both deposit and transfer
    amount = serializers.IntegerField()
    username = serializers.CharField()


class TransferSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    sender_username = serializers.CharField()
    reciever_username = serializers.CharField()
