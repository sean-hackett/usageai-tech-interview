from person_dashboard import *
import pytest
import bcrypt


@pytest.fixture
def demo_user():
    first = "Beom Joon"
    last = "Baek"
    email = "1234@columbia.edu"
    password = "password"
    DOB = "19960802"
    return User(first, last, DOB, email, password)


def test_check_pasword(demo_user):
    assert demo_user.check_pasword("password")

def test_display(demo_user):
    assert len(demo_user.display()) == 3

def test_create_user_list():
    assert True


