"""Main module for the Streamlit app"""
import requests
import streamlit as st
import random
import requests
from datetime import datetime
import numpy as np
import pandas as pd
import altair as alt

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

    country_codes = response.json()
    country_codes_only = [pair["key"] for pair in country_codes]

    return country_codes_only

def getHello():
    """ Gets Hello from a randomly generated IPv4 address usiing HelloSalut API

    Returns:
        A JSon file with "code" and "hello" representing language
        and hello in that language.

    Raises:
        requests.exceptions.RequestException: If the
        request to the HelloSalut API fails.
    """

    # Random IP Address
    ip = "{}.{}.{}.{}".format(*random.sample(range(0, 255), 4))
    URL = "https://fourtonfish.com/hellosalut/"
    PARAMS = {'ip': ip}
    try:
        response = requests.get(url=URL, params=PARAMS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    data = response.json()

    return data

def getNumberOfHolidays(country_code, durationYear=10):
    """ Returns a numpy array with the number of holidays in the country
        with the given country_code, by the duration defined in duration year.

    Param country_code:
        String of length two, denoting the country code

    Param durationYear:
        Integer, showing duration to display country's holidays. Default value 10 (last decade).

    Returns:
        Numpy array with year and number of holidays per year.
    """
    endYear = datetime.now().year
    startYear = endYear - durationYear

    year_list = np.arange(startYear, endYear+1)
    holiday_per_year = []
    url_add = [NAGER_API_BASE, "PublicHolidays", "{}", country_code]
    URL = "/".join(url_add)

    for index, year in enumerate(year_list):
        URL_year = URL.format(int(year))

        try:
            response = requests.get(url=URL_year)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        data = response.json()
        num_of_holidays = len(data)
        holiday_per_year.append(num_of_holidays)

    holiday_per_year = np.array(holiday_per_year)
    return year_list, holiday_per_year

def main():

    # Part 1
    hello = getHello()["hello"]

    st.markdown(hello)

    # Part 2
    country_codes = load_country_codes()

    country_code = st.selectbox('Select a country code', country_codes)

    st.markdown('You selected country code - ' + country_code)

    # Part 3
    year_list, holiday = getNumberOfHolidays(country_code)

    # turn numpy array to pandas dataframe
    numHolidaysPerYear_df = pd.DataFrame({"Year" : year_list,
                                          'Number of Holidays per Year': holiday})

    chart = alt.Chart(numHolidaysPerYear_df).mark_line().encode(
        x='Year',
        y='Number of Holidays per Year')
    st.altair_chart(chart)

if __name__ == '__main__':
    main()

