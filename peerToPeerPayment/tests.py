from django.test import TestCase
import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse

client = Client()


class TestCreateUser(TestCase):
    """ Test that a user can be created"""

    def setUp(self):
        pass

    def test_create_user(self):
        # tests that a user can be created successfuly
        # get API response
        newUser = {"email": "user1@gmail.com", "username": "user1"}
        response = client.post(reverse('add_user'), newUser)
        self.assertEqual(response.data, newUser | {"balance": 0})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_user(self):
        # tests that the proper error is returned when there is invalid data
        invalidUser = {}
        response = client.post(reverse('add_user'), invalidUser)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDeposit(TestCase):
    """ Test that a user can deposit into his wallet"""

    def setUp(self):
        user = {"email": "user2@gmail.com", "username": "user2"}
        client.post(reverse('add_user'), user)

    def test_deposit(self):
        # tests that a user can deposit into his wallet
        data = {"amount": 5000, "username": "user2"}
        response = client.post(reverse('deposit'), data)
        self.assertEqual(
            response.data, {"message": "deposit successfully", "balance": 5000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_deposit(self):
        # tests that the proper error is returned when there is invalid amount
        invalidData = {"amount": -5000, "username": "user2"}
        response = client.post(reverse('deposit'), invalidData)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "invalid amount"})


class TestWithdraw(TestCase):
    """ Test that a user can withdraw"""

    def setUp(self):
        user = {"email": "user3@gmail.com", "username": "user3"}
        client.post(reverse('add_user'), user)

    def test_withdraw(self):
        # tests that a user can withdraw successfully

        # we deposit 5000 into user3 account so we can test the withdrawal
        client.post(reverse('deposit'), {"username": "user3", "amount": 5000})

        data = {"amount": 4000, "username": "user3"}
        response = client.post(reverse('withdraw'), data)
        self.assertEqual(
            response.data, {"message": "withdraw successfully", "balance": 1000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_insufficient_funds(self):
        # tests that the proper error is returned when there is insufficient funds
        invalidData = {"amount": 15000, "username": "user3"}
        response = client.post(reverse('withdraw'), invalidData)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "insufficient funds"})

    def test_invalid_withdraw(self):
        # tests that the proper error is returned when there is invalid amount
        invalidData = {"amount": -5000, "username": "user3"}
        response = client.post(reverse('withdraw'), invalidData)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "invalid amount"})


class TestTransfer(TestCase):
    """ Test that a user can transfer to another user"""

    def setUp(self):
        # we create 2 users to test the transfer
        user1 = {"email": "john@gmail.com", "username": "john"}
        user2 = {"email": "doe@gmail.com", "username": "doe"}
        client.post(reverse('add_user'), user1)
        client.post(reverse('add_user'), user2)

    def test_transfer(self):
        # tests that a user can transfer successfully

        # we deposit 5000 into john's account
        data = {"amount": 5000, "username": "john"}
        client.post(reverse('deposit'), data)

        # we transfer 1000 from john to doe
        data = {"amount": 1000, "sender_username": "john", "reciever_username": "doe"}
        response = client.post(reverse('transfer'), data)

        self.assertEqual(
            response.data, {"message": "transfer successfully", "balance": 4000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check john's balance to confirm that the money left
        response = client.get(reverse('check_balance', kwargs={"username": "john"}))
        self.assertEqual(response.data, {"balance": 4000})

        # check doe's balance to confirm that the money was recieved
        response = client.get(reverse('check_balance', kwargs={"username": "doe"}))
        self.assertEqual(response.data, {"balance": 1000})

    def test_insufficient_funds(self):
        # tests that the proper error is returned when there is insufficient funds
        invalidData = {"amount": 10000, "sender_username": "john",
                       "reciever_username": "doe"}
        response = client.post(reverse('transfer'), invalidData)
        self.assertEqual(response.data, {"error": "insufficient funds"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
