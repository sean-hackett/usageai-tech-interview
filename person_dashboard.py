import requests
import streamlit as st
from dashboard import get_response

RANDOMUSER_API_BASE = 'https://randomuser.me/api'

class User:
    def __init__(self, response):
        self.first_name = response['name']['first']
        self.last_name = response['name']['last']
        self.dob = response['dob']['date']
        self.username = response['login']['username']
        self.hashed_password = response['login']['sha256']

def generate_users(n_users):
    base = RANDOMUSER_API_BASE
    params = f'?results={n_users}'

    response = get_response(base, params)
    users = [User(user_response) for user_response in response['results']]

    return users

def main():
    N_USERS = 100
    users = generate_users(N_USERS)
    print(users)

if __name__ == '__main__':
    main()