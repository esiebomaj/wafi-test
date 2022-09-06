from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from peerToPeerPayment.serializers import UserSerializer, DepositSerializer, TransferSerializer
# Create your views here.


users = {}


@api_view(['POST', ])
def create_user_view(request):
    serializer = UserSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data["username"]
    email = serializer.validated_data["email"]

    if username in users:
        return Response(
            {"error": "user already exist"}, status=status.HTTP_400_BAD_REQUEST)

    newUser = {
        "username": username,
        "email": email,
        "balance": 0,
    }

    users[username] = newUser

    return Response(newUser, status=status.HTTP_201_CREATED)


@api_view(['POST', ])
def deposit(request):
    serializer = DepositSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data["username"]
    amount = serializer.validated_data["amount"]

    if username not in users:
        return Response(
            {"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)

    if amount < 0:
        return Response(
            {"error": "invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

    user = users[username]

    user["balance"] += amount

    return Response(
        {"message": "deposit successfully", "balance": user["balance"]},
        status=status.HTTP_200_OK)


@api_view(['POST', ])
def withdraw(request):
    serializer = DepositSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data["username"]
    amount = serializer.validated_data["amount"]

    if username not in users:
        return Response(
            {"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)

    if amount < 0:
        return Response(
            {"error": "invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

    user = users[username]

    if amount > user["balance"]:
        return Response(
            {"error": "insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

    user["balance"] = user["balance"] - amount

    return Response(
        {"message": "withdraw successfully", "balance": user["balance"]},
        status=status.HTTP_200_OK)


@api_view(['POST', ])
def transfer(request):
    serializer = TransferSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    sender_username = serializer.validated_data["sender_username"]
    reciever_username = serializer.validated_data["reciever_username"]
    amount = serializer.validated_data["amount"]

    if (sender_username not in users) or (reciever_username not in users):
        return Response(
            {"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)

    if amount < 0:
        return Response(
            {"error": "invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

    reciever = users[reciever_username]
    sender = users[sender_username]

    if amount > sender["balance"]:
        return Response(
            {"error": "insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

    # if using db, this transactions should be atomic to ensure db integrity
    sender["balance"] = sender["balance"] - amount
    reciever["balance"] = reciever["balance"] + amount

    return Response(
        {"message": "transfer successfully", "balance": sender["balance"]},
        status=status.HTTP_200_OK)


@api_view(['GET', ])
def check_balance(request, username):

    if (username not in users):
        return Response(
            {"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)

    user = users[username]

    return Response({"balance": user["balance"]}, status=status.HTTP_200_OK)
