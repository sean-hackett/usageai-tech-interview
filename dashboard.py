"""Main module for the Streamlit dashboard app"""


import requests
import streamlit as st
import ipaddress
import random
import numpy as np
from datetime import datetime
from bokeh.plotting import figure


# Base URLs for the below APIs
NAGER_API_BASE = 'https://date.nager.at/api/v2'
SALUT_API_BASE = 'https://fourtonfish.com/hellosalut'


def random_ipv4():
    """Generates a random ip address
    
    Returns:
        The randomly generated ip address in string format
    """
    
    # Maximum IPv4 address : 2 ** 32 - 1
    ALL_ONES = ipaddress.IPv4Address._ALL_ONES
    ip_address = ipaddress.IPv4Address._string_from_ip_int(random.randint(0, ALL_ONES))
    
    return ip_address


@st.cache
def get_salutation(ip):
    """Gets the country specific salutation based on an IP address from the HelloSalut API
    
    Parameters: 
        - ip: string
            Random generated IP in string format
            
    Returns:
        The salutation for the country of the input ip parameter in string format
        
    Raises:
        SystemExit: If the request to the HelloSalut API fails.
    """

    # Join the base upi with ip URL parameter
    url = '/'.join([SALUT_API_BASE, '?ip=' + ip])
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    # Parse the response to a JSON format dict
    salutation_response = response.json()
    salutation = salutation_response['hello']

    return salutation


@st.cache
def load_country_codes():
    """Loads country codes available from the Nager.Date API
    
    Returns:
        A list of country codes. Each country code is
        a two character string.
        
    Raises:
        SystemExit: If the request to the Nager.Date API fails.
    """
    
    # Join the base URL with the proper end-point to fetch all country
    # codes
    url = '/'.join([NAGER_API_BASE, 'AvailableCountries'])
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    # Parse the response to a JSON format list
    country_codes = response.json()
    
    # Extract a list of only the country codes
    country_code_list = [dic['key'] for dic in country_codes]

    return country_code_list


@st.cache
def get_holidays(country_code):
    """Displays a line chart showing the number of holidays in that country, by year, for the last decade
    
    Parameters: 
        - country_code: Two-letter string
            Country code of the country selected in the drop-down list
            
    Returns:
        The number of holidays in the last decade in numpy array format
        
    Raises:
        SystemExit: If the request to the Nager.Date API fails.
    """
    
    today = datetime.today()
    decade_start_year = today.year-10
    
    # Create a numpy array with 10 rows and 2 columns of type int
    holidays = np.zeros((10,2), dtype=int)
    
    # Fill the decade years with number of holdiays
    # for the given country code
    for i in range(10):
        year = decade_start_year+i
        
        # Store the year in the first column
        holidays[i][0] = year
        
        # Join the API base URL with year and country_code URL parameters
        url = '/'.join([NAGER_API_BASE, 'PublicHolidays', str(year), country_code])
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
                raise SystemExit(e)
        
        # Format the response in JSON format
        holiday_list = response.json()
        
        # Store the number of holidays in the second column
        holidays[i][1] = len(holiday_list)
        
    return holidays


def main():
    """Displays a line chart showing the number of holidays in that country, by year, for the last decade
        
    Raises:
        SystemExit: If the call to get_salutation, load_country_codes or get_holidays methods fails.
    """
    
    # Generate a random IPv4 IP addr
    random_ip = random_ipv4()
    
    # Get a greeting based on the random IP
    greeting = get_salutation(random_ip)
    
    # Show greeting
    st.markdown(greeting)
    
    # Load all country codes
    country_codes = load_country_codes()
    country_codes = ['--'] + country_codes
    
    # Populate the selectbox and select a country code
    country_code = st.selectbox('Select a country code', country_codes)
    
    if country_code != '--':
        
        # Display the selected country code
        st.markdown('You selected country code - '+ country_code)

        # Get number of holidays in the last decade based on the country code
        holidays = get_holidays(country_code)

        # X-axis is the year
        x = holidays[:, 0]

        # Y-axis is the number of holidays
        y = holidays[:, 1]

        # Plot a line chart with the above data
        p = figure(title='Number of holidays in the last decade in ' + country_code, 
                   x_axis_label='Year', 
                   y_axis_label='Holiday Count')
        p.line(x, 
               y, 
               legend_label='# of holidays', 
               line_width=2)
        st.bokeh_chart(p, 
                       use_container_width=True)


if __name__ == '__main__':
    main()