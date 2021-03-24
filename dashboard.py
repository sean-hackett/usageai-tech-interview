"""Main module for the Streamlit app."""
import requests
import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime
from ipaddress import IPv4Address
from random import getrandbits


NAGER_API_BASE = "https://date.nager.at/api/v2"
SALUT_API_BASE = "https://fourtonfish.com/hellosalut"


def generate_random_ip() -> str:
    """Generate random IP address.

    Returns:
        A string representing an IPv4 address.
    """
    bits = getrandbits(32)
    addr = IPv4Address(bits)
    return str(addr)


@st.cache
def get_greeting(ip) -> str:
    """Greet user in local language based on ip_address.

    Returns:
        A string representing a greeting in local language.
            - example: "Hello" if ip_address is in the USA

    Raises:
        requests.exceptions.RequestException: If the
            request to the HelloSalut API fails.
    """
    salute_ip_endpoint = "?ip="
    url = "/".join([SALUT_API_BASE, salute_ip_endpoint + ip])

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    # Process the response to JSON and return greeting
    response_object = response.json()
    greeting = response_object["hello"]

    return greeting


@st.cache
def load_country_codes() -> list:
    """Load country codes available from the Nager.Date API.

    Returns:
        A list of country codes. Each country code is
        a two character string.

    Raises:
        requests.exceptions.RequestException: If the
            request to the Nager.Date API fails.
    """
    url = "/".join([NAGER_API_BASE, "AvailableCountries"])
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    # Process the response to JSON and return list of country codes
    country_codes = response.json()
    country_code_list = [dic["key"] for dic in country_codes]

    return country_code_list


@st.cache
def get_holidays(country_code, data_range=10):
    """Display line plot depicting total number of holidays for selected country by year.

    Parameters:
        - country_code: str
        - data_range: int (represents the number of years; defaults to 10 years)

    Returns:
        Pandas DataFrame containing the number of holidays in the last decade
            - number of holidays (y-axis)
            - by year (x-axis)
    """
    nager_holiday_endpoint = "PublicHolidays"

    today = datetime.today()
    decade_start_year = today.year - 10

    holidays = np.empty(data_range)

    for yr_offset in range(data_range):
        year = decade_start_year - yr_offset

        # Iteratively makes 10 API calls; each call returns a year's holiday data
        url = "/".join(
            [NAGER_API_BASE, nager_holiday_endpoint, str(year), country_code]
        )

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        holiday_count = len(response.json())
        holidays[yr_offset] = holiday_count

    # list of String(Years) to be used to build datatime indexing for panda's df
    years = [str(today.year - 10 + i) for i in range(data_range)]

    df = pd.DataFrame({"holiday_count": holidays, "year": years})

    # Convert index to datetime index
    datetime_series = pd.to_datetime(df["year"])
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    df2 = df.set_index(datetime_index)

    # we no longer need the column year
    df2.drop("year", axis=1, inplace=True)

    # return dataframe object with datetime indexing
    return df2


def main():
    random_ip_addr = generate_random_ip()
    greeting = get_greeting(random_ip_addr)
    st.markdown(greeting)

    country_codes = load_country_codes()

    country_code = st.selectbox("Select a country code", country_codes)

    # f-string resolves TypeError, which was likely caused by unintentional indention
    st.markdown(f"You selected country code - {country_code}")

    df = get_holidays(country_code)
    st.line_chart(df)


if __name__ == "__main__":
    main()
