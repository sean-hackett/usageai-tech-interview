import requests
import streamlit as st
from dashboard import get_response
import hashlib

RANDOMUSER_API_BASE = 'https://randomuser.me/api'

class User:
    def __init__(self, response):
        self.first_name = response['name']['first']
        self.last_name = response['name']['last']
        self.dob = response['dob']['date']
        self.username = response['login']['username']
        self.salt = response['login']['salt']
        self.hashed_password = response['login']['sha256']

def generate_users(n_users):
    base = RANDOMUSER_API_BASE
    params = f'?results={n_users}'

    response = get_response(base, params)
    users = dict()
    for user_response in response['results']:
        user = User(user_response)
        username = user.username
        users[username] = user

    return users

def validate_user(users, username, password):
    hashed_password = users[username].hashed_password
    return hashlib.sha256(password) == hashed_password

def main():
    N_USERS = 100
    users = generate_users(N_USERS)

    # For debugging:
    print([{username: f'{user.first_name} {user.last_name}'} for username, user in users.items()])

    # Login form
    # https://discuss.streamlit.io/t/is-there-a-way-to-create-a-form-with-streamlit/7057/2
    st.markdown('Please login:')
    username = st.text_input('Username')
    password = st.text_input('Password', type = 'password')
    user = None

    if username in users:
        user = users[username]

    if user and validate_user(users, username, password + user.salt):
        st.markdown(f'Welcome back, {user.first_name} {user.last_name}! Your DOB is {user.dob}')


if __name__ == '__main__':
    main()