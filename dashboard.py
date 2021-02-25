"""Main module for the Streamlit app"""
import requests
import streamlit as st
import html
import random

NAGER_API_BASE = 'https://date.nager.at/api/v2'


@st.cache
def load_country_codes():
    """Loads country codes available from the Nager.Date API

    Returns:
        A list of country codes. Each country code is
        a two character string.

    Raises:
        requests.exceptions.RequestException: If the
            request to the Nager.Date API fails.
    """


    url = '/'.join([NAGER_API_BASE, 'AvailableCountries'])
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    #### TODO - Process the response ####

    country_codes = response.json()

    #####################################

    return country_codes

def get_hello_message():
    """Creates a random IP address and makes a request to Hello Salut API to get hello in different languages based on IP address

    Returns:
        A HTML string to display Hello message on the webpage 
    Raises:
        requests.exceptions.RequestException: If the request to Hello Salut fails
    """
    p1 = random.randint(0, 255)
    p2 = random.randint(0, 255)
    p3 = random.randint(0, 255)
    p4 = random.randint(0, 255)

    #f-string python3 syntax
    # ip_addr = f"{p1}.{p2}.{p3}.{p4}"

    ip_addr = "{}.{}.{}.{}".format(p1, p2, p3, p4)
    try:
        msg_response = requests.get("https://fourtonfish.com/hellosalut/?ip={}".format(ip_addr))
        msg_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    #Languages like Hindi are not formated well on the webpage. Using htmlParser.unescape() to convert ASCII chars to HTML string.
    #htmlParser.unescape(hello_msg) to solve this issue. But I did not use it to solve this question due to module missing from the requirements. 
    hello_msg = msg_response.json()["hello"]
    return hello_msg


def main():
    #Saving the message string before displaying on the webpage
    final_msg = get_hello_message()

    st.markdown(final_msg)
    
    country_codes = load_country_codes()

    country_code = st.selectbox('Select a country code',
                                country_codes)

    st.markdown('You selected country code -', country_code)


if __name__ == '__main__':
    main()

