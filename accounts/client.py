from time import sleep
from unittest import result
from django.shortcuts import render
import requests
import json

from tenacity import retry

BASE_URL='http://127.0.0.1:8000/api/'
ENDPOINT = 'register/'
ENDPOINT1 = 'login/'
ENDPOINT2 = 'me/'
ENDPOINT2 = 'tools/'

# create/post new user into DB
def register_newUser():
    new_user={
        "username": "test123",
        "email":"test@gmail.com",
        "password":"test@123",
        "role":"employee"
    }
    headers = {'Content-Type': 'application/json'}
    response=requests.post(BASE_URL+ENDPOINT, data=json.dumps(new_user), headers=headers)
    if response:
        print("Registration Sucessfull.", response.json(), response.status_code)
    else:
        print("Registration Failed!", response.json(), response.status_code)

register_newUser()


# Login user 
def LoginUser():
    user={
        "username_or_email": "manish123", # or  "username_or_email":"manish@gmail.com",
        "password":"manish@123",
    }
    headers = {'Content-Type': 'application/json'}
    response=requests.post(BASE_URL+ENDPOINT1, data=json.dumps(user), headers=headers)
    if response:
        access_token = response.json().get('Access Token')
        print("Login Sucessfull.", "Access Token:", access_token, "Status:", response.status_code)
    else:
        print("Login Failed!", response.json(), "Status:", response.status_code)

# LoginUser()

# get resource from DB
def get_resources(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(BASE_URL+ENDPOINT2, headers=headers)
        response.raise_for_status()
        user_data = response.json()
        print("Logged-in user:", user_data)
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("Authentication failed. Please check your access token.")
        else:
            print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


# get_resources("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2OTc3NDE3LCJpYXQiOjE3MTY5NzU2MTcsImp0aSI6ImE3Y2VmZGFkMGRmZjQ1NTk4NzNmYWI0Y2ZjZTdhN2E0IiwidXNlcl9pZCI6Mn0.muHdwURrjkQUSV8FUTQlm50OMoRUhuI6VxRFKOK7R6Q")


# get resource from DB
def get_tool(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(BASE_URL+ENDPOINT2, headers=headers)
        response.raise_for_status()
        user_data = response.json()
        print("Tools:", user_data)
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("Authentication failed. Please check your access token.")
        else:
            print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# get_tool("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2OTc5NzU4LCJpYXQiOjE3MTY5Nzc5NTgsImp0aSI6IjlhYWRmNzgzMWM1ODQyYzFiNzAxODA1YWIyMzRlZDBmIiwidXNlcl9pZCI6Mn0.G_gqVls9wx5u4TwkVtIUFV8-mvs-Pp-utSIVUBupY9w")


