"""Module for the App class"""

#package imports
import requests
import streamlit as st
from json import JSONDecodeError

#local file imports
from users import User

class App:

    @staticmethod
    @st.cache(show_spinner = False)
    def api_get(url, payload = None):
        """Sends API get request.
        
        Takes in:
            API endpoint URL;
            Payload (dict object with key value pairs to send as url arguments) - defaults to None.

        Returns:
            Response from API endpoint.

        Raises:
            requests.exceptions.RequestException: If the
                request to the API fails.
        """

        try:
            response = requests.get(url, payload)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    @staticmethod
    @st.cache(show_spinner = False)
    def get_users_from_api(num_users):
        """Gets a specific number of fake users from the Random User Generator API.
    
        Takes in:
            The number of users to return.

        Returns:
            JSON object with the desired number of users.  
        """
        try:
            #Url params, using usageai seed and selecting only the needed attributes from the API.
            payload = {'results': num_users, 'seed': 'usageai', 'inc': 'name, dob, email, login'}
            response = App.api_get('https://randomuser.me/api/', payload)
            json = response.json()
            #Returning only the useful part of json response, the rest is unnecessary for this challenge.
            return json['results'] 
        #The response object sometimes raises a JSONDecodeError, in those cases, print to console and try again - shouldn't be necessary when using a seed.
        except JSONDecodeError:
            print('Error parsing JSON, trying again...') 
            App.get_users_from_api(num_users)

    @staticmethod
    def login():
        """Prompts user for login info, triggers further behaviour if login info is correct, otherwise it informs the user that authentication failed.
        """
        email = st.text_input('Email')
        if email:
            password = st.text_input('Password')
            if password:
                user = User.authenticate(email, password)
                if user:
                    App.display_info(user)
                else:
                    st.write('Authentication failed')

    @staticmethod
    def display_info(user):
        st.write('First name: ' + user.first_name)
        st.write('Last name: ' + user.last_name)
        st.write('DOB' + user.dob)