"""Main Module for the Streamlit App"""

#local file imports
from users import User
from app import App

def main():
    #Creating instance of App class
    app = App()

    #Handling user creation
    users = app.get_users_from_api(100)
    User.create_users(users)

    #Handling login
    app.login()

if __name__ == '__main__':
    main()