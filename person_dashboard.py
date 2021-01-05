import requests
import streamlit as st
import pickle
import bcrypt
import os

RandomUserGeneratorURL = "https://randomuser.me/api/"
display_list = ["First Name", "Last Name", "dob"]


class User:
    """
    Class for User data. Has functions to create and check for passwords.
    """
    def __init__(self, first_name, last_name, dob, email, plain_text_password):
        self.first_name = first_name
        self.last_name = last_name
        self.DOB = dob
        self.email = email
        self.password = 0

        self.generate_hashed_password(plain_text_password)

    def generate_hashed_password(self, plain_text_password):
        """ Create password from plain_text_password. Bcrypt also automatically generate salt.

        Param plain_text_password:
            String.
        """
        # generate hashed password first time
        hashed = bcrypt.hashpw(plain_text_password.encode('UTF-8'), bcrypt.gensalt())
        self.password = hashed

    def check_pasword(self, input_password):
        """ Check if input password is correct with the hash password.

        Param input_password:
            Password to check with hash password.

        Return:
            True if password matches
            False if it does not.
        """
        if bcrypt.checkpw(input_password.encode('UTF-8'), self.password):
            return True
        else:
            return False

    def display(self):
        """ Used to display user information

        Return:
            A list of first name, last name, and DOB
        """
        return [self.first_name, self.last_name, self.DOB]


def createUserDict(num_of_users=100, seed="usageai"):
    """ Create user dictionary using RANDOM USER GENERTOR API
        key: email
        value: User object

    Param num_of_users: number of users to generate using RANDOM USER GENERTOR API
    Param seed: seed value to be sent to RANDOM USER GENERTOR API

    Return: User dictionary

    Raises:
        requests.exceptions.RequestException: If the
        request to the RANDOM USER GENERTOR API fails.
    """
    PARAMS = {"results": num_of_users, "seed": seed}
    try:
        response = requests.get(url=RandomUserGeneratorURL, params=PARAMS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    data = response.json()
    assert len(data["results"]) == num_of_users

    user_dictionary = dict()
    for result in data["results"]:
        email, user = createUser(result)
        user_dictionary[email] = user

    assert len(user_dictionary) == num_of_users

    return user_dictionary


def createUser(result):
    """ Create User object using result json file

    Param result: json file of randomly generated user profile
    Return:
        email: String, email of user
        user: User object
    """
    first_name = result["name"]["first"]
    last_name = result["name"]["last"]
    email = result["email"]
    password = result["login"]["password"]
    dob = result["dob"]["date"][:10]
    user = User(first_name=first_name, last_name=last_name, dob=dob, email=email, plain_text_password=password)
    return email, user


# Helper functions to load and save User dictionary
def saveUsers(data, filename="hundreadUsers.pkl"):
    # Save data in pickle
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def loadUsers(filename="hundreadUsers.pkl"):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data


if __name__ == '__main__':
    if not os.path.isfile("hundreadUsers.pkl"):
        # The user file not created
        print("Creating User Dict")
        user_dictionary = createUserDict()
        saveUsers(user_dictionary)
    else:
        # Load pre-existing user dictionary
        print("Loading User Dict")
        user_dictionary = loadUsers()

    #print(user_dictionary["ismael.bravo@example.com"].display())

    st.title("Welcome! Please enter your email and password")
    user_email = st.text_input("Email")
    user_password = st.text_input("Password")

    # find corresponding user
    if st.button("Log in"):
        with st.spinner("Loading ..."):
            if user_email in user_dictionary:
                user = user_dictionary[user_email]
                if user.check_pasword(user_password):
                    st.success('Correct Password!')
                    data = user.display()
                    for field, d in zip(display_list, data):
                        st.text(field + " : " + d)
                else:
                    st.error('Incorrect Log in. Please try again.')
            else:
                st.error('Incorrect Log in. Please try again.')