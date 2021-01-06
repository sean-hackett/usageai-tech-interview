"""Main module for the Streamlit app"""
import requests
import streamlit as st

NAGER_API_BASE = 'https://date.nager.at/api/v2'
SALUT_API_BASE = 'https://fourtonfish.com/hellosalut'

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

    country_codes = [country['key'] for country in response.json()]


    #####################################

    return country_codes

def generate_random_ip():
    ''' Generate a valid IPv4 address (str)
     that obeys this format: http://www.doc.gold.ac.uk/~mas01rk/Teaching/CIS110/notes/IP-Address.html

     Inputs:
        (None)

     Returns:
        ip (str) The randomly generated IP address

     '''

    from random import randint

    N_PARTS = 4 # e.g.: 8.8.8.8
    RANGE_MIN, RANGE_MAX = 0, 255

    def validate_ip(parts):
        if parts[0] == 10:
            return False
        elif parts[0] == 172 and 16 <= parts[1] <= 31:
            return False
        elif parts[0] == 192 and parts[1] == 168:
            return False
        else:
            return True

    while True:
        parts = [randint(RANGE_MIN, RANGE_MAX) for i in range(N_PARTS)]
        if validate_ip(parts):
            ip = '.'.join([str(part) for part in parts])
            return ip

def get_salutation(ip):
    ''' Get salutation (str) based on an IP address (str)

    Inputs:
        ip (str) The IP address for which the salutation is desired

    Returns:
        salutation (str) The salutation for the IP address

    '''

    url = '/'.join([SALUT_API_BASE, f'?ip={ip}'])
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    salutation = response.json()['hello']

    return salutation

def main():
    # Salutation
    ip = generate_random_ip()
    st.markdown(get_salutation(ip))

    # Country codes
    country_codes = load_country_codes()

    country_code = st.selectbox('Select a country code',
                                country_codes)

    st.markdown('You selected country code -', country_code)


if __name__ == '__main__':
    main()

