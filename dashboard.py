"""Main module for the Streamlit app"""
import requests
import streamlit as st
from random import randint
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

NAGER_API_BASE_v1 = 'https://date.nager.at/api/v1/Get'
NAGER_API_BASE_v2 = 'https://date.nager.at/api/v2'
SALUT_API_BASE = 'https://fourtonfish.com/hellosalut'

def get_response(base, params):
    ''' Gets the response of an API request

    Inputs:
        base (str) The API base
        params (str) The API params

    Returns:
        response.json() (dict) The response

    '''


    # E.g.: 'https://fourtonfish.com/hellosalut' + '/' + '?ip=8.8.8.8'
    url = base + '/' + params

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    return response.json()

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

    base = NAGER_API_BASE_v2
    params = 'AvailableCountries'
    country_codes = [country['key'] for country in get_response(base, params)]

    return country_codes

def generate_random_ip():
    ''' Generate a valid IPv4 address (str)
     that obeys this format: http://www.doc.gold.ac.uk/~mas01rk/Teaching/CIS110/notes/IP-Address.html

     Inputs:
        (None)

     Returns:
        ip (str) The randomly generated IP address

     '''

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

    base = SALUT_API_BASE
    params = f'?ip={ip}'
    salutation = get_response(base, params)['hello']

    return salutation

@st.cache
def get_holidays(country_code, n_last_years, this_year = datetime.now().year):
    ''' Get the holidays (dataframe) based on params

        Inputs:
            country_code (str) Which country are we looking at
            n_last_years (int) How many past years do we want to grab the n_holidays for
            this_year (int) The current year

        Returns:
            n_holidays_in_year (dataframe) The number of holidays, indexed by their year numbers (e.g. 2021)

        '''

    base = NAGER_API_BASE_v1

    n_holidays_in_year = pd.DataFrame(columns = ['year', 'n_holidays']).set_index('year')

    for year in range(this_year - n_last_years + 1, this_year + 1):
        params = f'{country_code}/{year}'
        n_holidays_in_year.loc[int(year), 'n_holidays'] = len(get_response(base, params))

    return n_holidays_in_year

def build_holidays_chart(country_code, n_last_years, this_year = datetime.now().year):
    ''' Build the holidays chart

        Inputs:
            country_code (str) Which country are we looking at
            n_last_years (int) How many past years do we want to grab the n_holidays for
            this_year (int) The current year

        Returns:
            chart (st.line_chart) The line chart of the number of holidays, indexed by year (e.g. 2021)

        '''

    def build_chart(data):
        return st.line_chart(data)

    n_holidays_in_year = get_holidays(country_code, n_last_years, this_year)
    chart = build_chart(n_holidays_in_year)

    # Manual testing, because I got rate-limited by the API:
    # n_holidays_in_year = pd.DataFrame(columns = ['year', 'n_holidays']).set_index('year')
    # n_holidays_in_year.loc[2020, 'n_holidays'] = 5
    # n_holidays_in_year.loc[2021, 'n_holidays'] = 6

    return chart


def main():
    # Salutation
    ip = generate_random_ip()
    st.markdown(get_salutation(ip))

    # Country codes
    country_codes = load_country_codes()

    country_code = st.selectbox('Select a country code',
                                country_codes)

    st.markdown(f'You selected country code - {country_code}')

    N_LAST_YEARS = 10
    build_holidays_chart(country_code, N_LAST_YEARS)

if __name__ == '__main__':
    main()

