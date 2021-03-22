"""Main module for the Streamlit app"""
import json
import urllib.request
from random import randint

import numpy as np
import pandas as pd
import requests
import streamlit as st

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

    return [c['key'] for c in country_codes]


def generate_random_ip():
    return ".".join(str(randint(0, 255)) for _ in range(4))


def main():
    random_ip = generate_random_ip()
    response = urllib.request.urlopen(f"https://fourtonfish.com/hellosalut/?ip={random_ip}").read().decode('utf-8')
    st.markdown(json.loads(response)['hello'])

    country_codes = load_country_codes()

    country_code = st.selectbox('Select a country code',
                                country_codes)

    st.markdown(f'You selected country code - {country_code}')

    years_range = 10
    holiday_counts = np.empty(years_range)

    start_year = 2012
    # TODO async or cache
    for year_offset in range(years_range):
        year = start_year + year_offset

        response = urllib.request.urlopen(
            f"https://date.nager.at/Api/v2/PublicHolidays/{year}/{country_code}").read().decode('utf-8')

        holiday_count = len(json.loads(response))
        holiday_counts[year_offset] = holiday_count

    df = pd.DataFrame({"HolidayCount": holiday_counts})

    st.line_chart(df, width=0, height=0, use_container_width=True)


if __name__ == '__main__':
    main()
