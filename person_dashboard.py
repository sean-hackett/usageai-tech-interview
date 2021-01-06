import requests
import streamlit as st
from dashboard import get_response
import hashlib
from sqlite_utils import DB

RANDOMUSER_API_BASE = 'https://randomuser.me/api'

def hash256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

class User:
    def __init__(self, ):
        pass

    def init_response(self, response):
        self.username = response['login']['username']

        self.first_name = response['name']['first']
        self.last_name = response['name']['last']
        self.dob = response['dob']['date']
        self.salt = response['login']['salt']

        self.hashed_password = hash256(response['login']['password'] + self.salt)

    def init_list(self, list_):
        self.username, self.first_name, self.last_name, self.dob, self.salt, self.hashed_password = list_


@st.cache
def generate_users(n_users):
    ''' Generate n_users users by making an API request and instantiating the users as objects

    Inputs:
        n_users (int) Number of users to generate

    Returns:
        users (List[User]) A list of user objects that were generated

    '''


    base = RANDOMUSER_API_BASE
    params = f'?results={n_users}'

    response = get_response(base, params)
    users = dict()
    for user_response in response['results']:
        user = User()
        user.init_response(user_response)
        username = user.username
        users[username] = user

        # For debugging:
        print([{username: f'{user.first_name} {user.last_name}, {user_response["login"]["password"]}'} for username, user in users.items()])
        print('\n')

    return users

@st.cache
def validate_user(user, attempted_password):
    ''' Validate the user's username and password

    Inputs:
        users (List[User]) List of users we have already generated
        username (str) The username the user entered
        password (str) The password the user entered

    Returns:
        (bool) Whether the entered password, when hashed along with the salt,
                matches the user's hashed password

    '''

    hashed_password = user.hashed_password
    attempted_hash = hash256(attempted_password + user.salt)

    print(f'hashed_password = {hashed_password}')
    print(f'attempted_hash = {attempted_hash}')
    return attempted_hash == hashed_password

def update_db(db, users):
    # Create db and table if not exists
    db.create_db()
    db.execute('''
               CREATE TABLE IF NOT EXISTS users
                (username, first_name, last_name, dob, salt, hashed_password)
               ''')

    # Insert users
    insertions = [(user.username, user.first_name, user.last_name, user.dob, user.salt, user.hashed_password) \
               for username, user in users.items()]
    db.executemany('''
                   INSERT INTO users values (?, ?, ?, ?, ?, ?)
                   ''', insertions)

    # Close connection
    db.close()

def get_row_from_db(db, username):
    db.connect()
    statement = '''
                SELECT * FROM users WHERE username = ? LIMIT 1
                '''
    insertions = (username,)
    db.execute(statement, insertions)

    return db.fetched

def main():
    N_USERS = 100
    DB_PATH = 'users.sqlite3'

    # This DB is cumulative: it contains all previously generated users
    db = DB(DB_PATH)
    users = generate_users(N_USERS)
    if users:
        update_db(db, users)

    # Login form
    # https://discuss.streamlit.io/t/is-there-a-way-to-create-a-form-with-streamlit/7057/2
    st.markdown('Please login:')
    username = st.text_input('Username')
    password = st.text_input('Password', type = 'password')
    user = None

    if username and password:
        row = get_row_from_db(db, username)
        if row:
            user = User()
            user.init_list(row[0])
        else:
            st.markdown('That username doesn\'t exist! Please try again.')

    if user:
        if validate_user(user, password):
            st.markdown(f'Welcome back, {user.first_name} {user.last_name}! Your DOB is {user.dob}')
        else:
            st.markdown('Incorrect username or password! Please try again.')

if __name__ == '__main__':
    main()