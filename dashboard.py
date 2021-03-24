"""Main module for the Streamlit app."""
import requests
import streamlit as st
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

    # Process the response to JSON and return list of country codes
    country_codes = response.json()
    country_code_list = [dic["key"] for dic in country_codes]

    return country_code_list


def main():
    random_ip_addr = generate_random_ip()
    greeting = get_greeting(random_ip_addr)
    st.markdown(greeting)

    country_codes = load_country_codes()

    country_code = st.selectbox("Select a country code", country_codes)

    st.markdown("You selected country code -", country_code)


if __name__ == "__main__":
    main()
