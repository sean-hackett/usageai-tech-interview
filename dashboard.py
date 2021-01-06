"""Main module for the Streamlit app"""

#Imports
import requests
import streamlit as st
from faker import Faker
faker = Faker()
import datetime
import numpy as np
import pandas as pd

#Top-level vars
NAGER_API_BASE = 'https://date.nager.at/api/v2'

@st.cache(show_spinner = False)
def api_get(url):
    """Sends API get request.
    
    Takes in:
        API endpoint URL.

    Returns:
        Response from API endpoint.

    Raises:
        requests.exceptions.RequestException: If the
            request to the API fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

@st.cache(show_spinner = False)
def generate_salutation():
    """Generates a salutation using the Hello, Salut! API.

    Returns:
        Salutation in the language corresponding to a randomly generated IP address's location.

    Raises:
        requests.exceptions.RequestException: If the
            request to the Hello, Salut! API fails.
    """
    ip = faker.ipv4()
    response = api_get('https://fourtonfish.com/hellosalut/?ip='+ip)
    salutation = response.json()['hello']
    return salutation

@st.cache(show_spinner = False)
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
    response = api_get(url)

    #### TODO - Process the response ####

    country_codes = response.json()
    country_codes = [code['key'] for code in country_codes]

    #####################################

    return country_codes

@st.cache(show_spinner = False)
def get_holidays(country_code):
    """Loads country codes available from the Nager.Date API

    Takes in:
        A country code string.

    Returns:
        A Pandas dataframe with the number of holidays per year for the last decade in the given country.

    Raises:
        requests.exceptions.RequestException: If the
            request to the Nager.Date API fails.
    """
    current_year = datetime.datetime.now().year

    x_years = np.empty(shape = (11), dtype = int)
    y_holidays = np.empty(shape = (11), dtype = int)

    for index,year in enumerate(range(current_year - 10, current_year + 1)):
        url = '/'.join(['https://date.nager.at/Api/v1/Get', str(country_code), str(year)])
        response = api_get(url)

        x_years[index] = year
        num_holidays = len(response.json())
        y_holidays[index] = num_holidays

    df = pd.DataFrame({'holidays': y_holidays}, index = x_years)
    return df


def main():
    salutation = generate_salutation()
    st.markdown(salutation)

    country_codes = load_country_codes()

    country_code = st.selectbox('Select a country code',
                                country_codes)

    st.markdown('You selected country code - ' + country_code)

    holidays = get_holidays(country_code)

    st.line_chart(holidays)


if __name__ == '__main__':
    main()

