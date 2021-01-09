"""Main module for the Streamlit person_dashboard app"""


import hashlib
import binascii
from mongodb import Db


class User():
    """A class used to represent a user,
    fetched from the randomuser API
    """

        
    def __init__(self, data = None):
        """Create a User object with the provided data
        
        Parameters: 
            - data: dict, optional
                Fetched from the randomuser API
        """
        
        # If data is provided, fill in the objects
        if data:
            self.first_name = data['name']["first"]
            self.last_name = data['name']["last"]
            self.dob = data['dob']["date"]
            self.email = data['email']
            self.salt = data['login']['salt']
            self.stored_password = self.hash_password(data['login']['salt'], data['login']['password'])
            
        # Else fill with None
        else:
            self.first_name = None
            self.last_name = None
            self.dob = None
            self.email = None
            self.salt = None
            self.stored_password = None
        
        
    def verify_password(self, provided_password):
        """Verify a stored password against one provided by user
        
        Parameters: 
            - provided_password: string
                Password provided by the user on the login page
            
        Returns:
            True if the provided_password matches the stored_password else False
            """
    
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), self.salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')

        return pwdhash == self.stored_password
    
    
    @classmethod
    def hash_password(cls, salt, password):
        """Hash a password for storing.
        
        Parameters: 
            - salt: string
                User salt fetched from randomuser API
            - password: string
                User password fetched from randomuser API
            
        Returns:
            The hashed password string
        """

        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash)

        return pwdhash.decode('ascii')
    
    
    def get_dict(self):
        """Get the object in dictionary representation
        
        Returns:
            The dictionary representation of User object
        """
        
        user_dict = { "first_name": self.first_name, 
                  "last_name": self.last_name, 
                  "dob": self.dob, 
                  "email": self.email, 
                  "salt": self.salt, 
                  "stored_password": self.stored_password 
                 }
        
        return user_dict
    
    
    @classmethod
    def users_exist(cls):
        """Check if users exist in the db.
        
        Returns:
            True if Users collection exists in the db else False
            
        Raises:
            SystemExit: If the database call fails.
        """
        
        db = Db()
        
        return db.get_one_doc() != None
        
        
    @classmethod
    def save_users(cls, user_list):
        """Save a list of users in the db.
        
        Parameters: 
            - user_list: list
                A list of dictionary representation of Users
                
        Raises:
            SystemExit: If the database call fails.
        """

        db = Db()
        dict_list = [user.get_dict() for user in user_list]
        db.save_users(dict_list)
        
    @classmethod
    def get_user_from_dict(cls, user_dict):
        """Create a User object from dict representation.
        
        Parameters: 
            - user_dict: dictionary
                Dictionary representation of a User
                
        Returns:
            The User object
        """
        
        user  = User()
        user.first_name = user_dict['first_name']
        user.last_name = user_dict['last_name']
        user.dob = user_dict['dob']
        user.email = user_dict['email']
        user.salt = user_dict['salt']
        user.stored_password = user_dict['stored_password']
        
        return user
        
    @classmethod
    def get_user(cls, email):
        """Save a list of users in the db.
        
        Parameters: 
            - email: string
                Email id of the user
                
        Returns:
            List of User objects if the email id exists else None
            
        Raises:
            SystemExit: If the database call fails.
        """

        db = Db()
        dict_list = db.find_users(email)
        if dict_list:
            user_dict = dict_list[0]
            return User.get_user_from_dict(user_dict)
        return None