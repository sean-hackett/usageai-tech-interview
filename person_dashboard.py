"""Login module for the Streamlit app"""
import hashlib
import json

import requests
import streamlit as st

from user import User


@st.cache
def load_users(num_users):
    users = {}  # dict of email: user_info

    randomuser_api_seed = "usageai"
    response = requests.get(f'https://randomuser.me/api/?seed={randomuser_api_seed}&results={num_users}')

    if response.ok:
        data = json.loads(response.content)

        for d in data['results']:
            users[d['email']] = User(d['email'],
                                     d['login']['password'],
                                     d['login']['salt'],
                                     d['name']['first'],
                                     d['name']['last'],
                                     d['dob']['date'])

        return users
    else:
        response.raise_for_status()


def main():
    users = load_users(100)

    email = st.text_input("Email")
    password = st.text_input("Password", type='password')

    if st.button('Login'):
        if email in users:
            if users[email].password == hashlib.sha512(users[email].salt + password.encode('utf-8')).hexdigest():
                st.markdown(f'First Name: {users[email].first_name}')
                st.markdown(f'Last Name: {users[email].last_name}')
                st.markdown(f'Date of Birth String: {users[email].date_of_birth}')

            else:
                st.markdown('Incorrect Password')

        else:
            st.markdown('User Not Found')


if __name__ == '__main__':
    main()
