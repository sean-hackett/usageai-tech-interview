"""Main module for the Streamlit person_dashboard app"""


import requests
import streamlit as st
import dateutil.parser
from user import User


# Base URL for the randomuser api to fetch only the required details
RANDOM_API_URL = 'https://randomuser.me/api/?seed=usageai&results=100&inc=name,email,login,dob'


@st.cache(suppress_st_warning=True, show_spinner=False)
def load_random_users():
    """Loads random users available from the Random User Generator API
    
    Returns:
        A list of users. Each user is a dictionary of required fields.
        
    Raises:
        SystemExit: If the
            request to the Nager.Date API fails.
    """
    
    data_load_state = st.text('Loading user data...')
    
    try:
        response = requests.get(RANDOM_API_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    data_load_state.text('Encrypting sensitive fields...')
    
    # Get random user data from API
    users = response.json()
    user_list = users['results']
    
    hashed_user_list = []
    
    # Create a list of User objects with hashed password
    for user_data in user_list:
        hashed_user_list.append(User(user_data))
        
    data_load_state.empty()
    
    return hashed_user_list


@st.cache(show_spinner=False)
def get_user_dict(user_list):
    """Loads random users available from the Random User Generator API
    
    Parameters: 
        - user_list: list
            List of User objects
    
    Returns:
        A dictionary of all User objects with email id as the key
    """
    
    user_dict = {}
    for user in user_list:
        user_dict[user.email] = user
        
    return user_dict


def generate_login_block():
    """ Create two empty blocks to hold the email id and password textboxes
    
    Returns:
        A list of the two created blocks
    """
    
    blocks = [st.empty(), st.empty()]
    
    return blocks


def clean_blocks(blocks):
    """ Empty the list of blocks of all content
    
    Parameters: 
        - blocks: list
            List of blocks
    """
    
    for block in blocks:
        block.empty()


def login(blocks):
    """ Get the email id and password
    
    Parameters: 
        - blocks: list
            List of blocks
            
    Returns:
        The email id and password entered by the user
    """
    
    return blocks[0].text_input('Email'), blocks[1].text_input('Password', type="password")


def main():
    """Displays a user details if login is successful
        
    Raises:
        SystemExit: If the call to users_exist, load_random_users, save_users or get_user methods fails.
    """
    
    # Generate blocks to hold input boxes
    login_blocks = generate_login_block()
    
    # Get the email id and password entered by the user
    provided_email, provided_password = login(login_blocks)
    
    try:
        # If users do not exist in the database
        # fetch from randomuser api and save in db
        if not User.users_exist():
            user_list = load_random_users()
            User.save_users(user_list)
        
        # If email is not empty
        if provided_email:
            user = User.get_user(provided_email)
            
            # If a user exists with the provided email
            if user:
                
                # If password is not empty
                if provided_password:
                    
                    # Verify the password and display user details
                    if user.verify_password(provided_password):
                        clean_blocks(login_blocks)
                        st.markdown('**Firstname** : '+ user.first_name)
                        st.markdown('**Lastname** : '+ user.last_name)
                        dob = dateutil.parser.parse(user.dob)
                        st.markdown('**DOB** : '+ dob.strftime('%m/%d/%Y'))
                        
                    # Else password in not valid
                    else:
                        st.info("Please enter a valid password!")
                        
            # Else email id is not valid
            else:
                st.info("Email does not exist. Please enter a valid email!")
                
    # In case the api service is not available
    except SystemExit:
        st.error("Service Temporarily Unavailable for randomuser.me API! Please refresh the page.")

   
if __name__ == '__main__':
    main()