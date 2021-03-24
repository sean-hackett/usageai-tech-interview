"""Main module for the Streamlit app."""
import requests
import streamlit as st

NAGER_API_BASE = "https://date.nager.at/api/v2"


@st.cache
def load_country_codes():
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

    # TODO - Process the response ####

    country_codes = response.json()

    #####################################

    return country_codes


def main():
    st.markdown("Have fun!")

    country_codes = load_country_codes()

    country_code = st.selectbox("Select a country code", country_codes)

    st.markdown("You selected country code -", country_code)


if __name__ == "__main__":
    main()
