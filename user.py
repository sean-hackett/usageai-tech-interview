import hashlib


class User:

    def __init__(self, email, password, salt, first_name, last_name, date_of_birth):
        self._email = email
        # self._password = hash(password)
        self._password = hashlib.sha512(salt.encode('utf-8') + password.encode('utf-8')).hexdigest()
        self._salt = salt.encode('utf-8')
        self._first_name = first_name
        self._last_name = last_name
        self._date_of_birth = date_of_birth

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def salt(self):
        return self._salt

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def date_of_birth(self):
        return self._date_of_birth
