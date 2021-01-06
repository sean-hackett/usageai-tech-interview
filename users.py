"""Module for the User class"""

#package imports
import hashlib

class User:
    all = []

    def __init__(self, json):
        """
        Initializes a User object.

        Takes in:
            A fake user JSON object from the Random User Generator Api.

        Returns:
            A User object with a first name, last name, date of birth, email, salt, and hashed password (with md5 encryption).
        """
        self.first_name = json['name']['first']
        self.last_name = json['name']['last']
        self.dob = json['dob']['date']
        self.email = json['email']
        self.salt = json['login']['salt']
        self.hashed_password = json['login']['md5'] #using the md5 cryptographic hash function
        User.all.append(self)

    @classmethod
    def create_users(cls, users_json):
        """Creates a user object for each user inside a JSON object with multiple user JSONs.

        Takes in:
            A JSON object with multiple user JSONs.

        Returns:
            None.
        """
        for user in users_json:
            cls(user)    
    
    @classmethod
    def find_by_email(cls, email):
        """Finds an existing user object by its email attribute.

        Takes in:
            An email string.

        Returns:
            An existing user object whose email address corresponds to te given string.

        """
        for user in cls.all:
            if user.email == email:
                return user

    @classmethod
    def authenticate(cls, email, password):
        """Authenticates inputted email and password by matching these to an existing user object.

        Takes in:
            An email string and a password string.

        Returns:
            A user object (if authentication is successfull); False (if authentication fails).
        """
        user = cls.find_by_email(email)
        if user:
            salted = password + user.salt
            hashed = hashlib.md5(bytes(salted, encoding = 'utf-8'))
            if hashed.hexdigest() == user.hashed_password:
                return user
            else:
                return False
        else:
            return False