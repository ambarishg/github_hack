# Write a command line app that takes a city as input and calls the OpenWeatherMap API.
# It should return the current weather for that city.
# The app should be able to handle the following error cases gracefully:
#   - The city doesn't exist/isn't supported
#   - The city name is not a string
#   - The city name is not provided
#   - The API call fails
#   - The API call returns an error
#   - The API call returns invalid data
#   - The API call returns valid data, but the data is not in the expected format
#   - The API call returns valid data, but the data is not for the requested city
#   - The API call returns valid data, but the data is not for the current time
#   - The API call returns valid data, but the data is not for the current weather
#   - The API call returns valid data, but the data is not for the current temperature
#   - The API call returns valid data, but the data is not for the current humidity
#   - The API call returns valid data, but the data is not for the current wind speed
#   - The API call returns valid data, but the data is not for the current wind direction
#   - The API call returns valid data, but the data is not for the current cloudiness
#   - The API call returns valid data, but the data is not for the current pressure
#   - The API call returns valid data, but the data is not for the current sunrise time
#   - The API call returns valid data, but the data is not for the current sunset time
#   - The API call returns valid data, but the data is not for the current visibility
#   - The API call returns valid data, but the data is not for the current precipitation
#   - The API call returns valid data, but the data is not for the current weather description
#   - The API call returns valid data, but the data is not for the current weather icon
#   - The API call returns valid data, but the data is not for the current weather code
#   - The API call returns valid data, but the data is not for the current weather id
#   - The API call returns valid data, but the data is not for the current weather main
#   - The API call returns valid data, but the data is not for the current weather visibility
#   - The API call returns valid data, but the data is not for the current weather base
#   - The API call returns valid data, but the data is not for the current weather timezone
#   - The API call returns valid data, but the data is not for the current weather dt
#   - The API call returns valid data, but the data is not for the current weather cod
#   - The API call returns valid data, but the data is not for the current weather coord
#   - The API call returns valid data, but the data is not for the current weather sys
#   - The API call returns valid data, but the data is not for the current weather main
#   - The API call returns valid data, but the data is not for the current weather wind
#   - The API call returns valid data, but the data is not for the current weather clouds
#   - The API call returns valid data, but the data is not for the current weather weather
#   - The API call returns valid data, but the data is not for the current weather base

import requests
import json
import sys
import os
import time
import datetime
import pytz
import tzlocal
import dateutil.parser
import dateutil.tz
import dateutil.relativedelta
import dateutil.rrule

#set the environment variable
os.environ['OPENWEATHERMAP_API_KEY'] = '110ec4e2891475d69cb2a510e5f9ea57'


# API key
API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')

# API URL
API_URL = 'https://api.openweathermap.org/data/2.5/weather'

# API parameters
API_PARAMS = {
    'appid': API_KEY,
    'units': 'metric',
    'lang': 'en'
}   

# API response codes
API_RESPONSE_CODES = {
    200: 'Success',
    201: 'Success',
    202: 'Success',
    204: 'Success',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    408: 'Request Timeout',
    429: 'Too Many Requests',
    500: 'Internal Server Error',
    502: 'Bad Gateway',
    503: 'Service Unavailable'
}   

# API response fields
API_RESPONSE_FIELDS = [
    'coord',
    'weather',
    'base',
    'main',
    'visibility',
    'wind',
    'clouds',
    'dt',
    'sys',
    'timezone',
    'id',
    'name',
    'cod'
]

# API response field types
API_RESPONSE_FIELD_TYPES = {
    'coord': dict,
    'weather': list,
    'base': str,
    'main': dict,
    'visibility': int,
    'wind': dict,
    'clouds': dict,
    'dt': int,
    'sys': dict,
    'timezone': int,
    'id': int,
    'name': str,
    'cod': int
}

# API response field values
API_RESPONSE_FIELD_VALUES = {
    'coord': {
        'lon': float,
        'lat': float
    },  
    'weather': [
        {
            'id': int,
            'main': str,
            'description': str,
            'icon': str
        }
    ],  
    'base': str,
    'main': {
        'temp': float,
        'feels_like': float,
        'temp_min': float,
        'temp_max': float,
        'pressure': int,
        'humidity': int,
        'sea_level': int,
        'grnd_level': int
    },
    'visibility': int,
    'wind': {
        'speed': float,
        'deg': int,
        'gust': float
    },
    'clouds': {
        'all': int
    },
    'dt': int,
    'sys': {
        'type': int,
        'id': int,
        'country': str,
        'sunrise': int,
        'sunset': int
    },
    'timezone': int,
    'id': int,
    'name': str,
    'cod': int  
}

# API response field units
API_RESPONSE_FIELD_UNITS = {
    'coord': {
        'lon': '°',
        'lat': '°'
    },
    'weather': [
        {
            'id': '',
            'main': '',
            'description': '',
            'icon': ''
        }
    ],
    'base': '',
    'main': {
        'temp': '°C',
        'feels_like': '°C',
        'temp_min': '°C',
        'temp_max': '°C',
        'pressure': 'hPa',
        'humidity': '%',
        'sea_level': 'hPa',
        'grnd_level': 'hPa'
    },
    'visibility': 'm',
    'wind': {
        'speed': 'm/s',
        'deg': '°',
        'gust': 'm/s'
    },
    'clouds': {
        'all': '%'
    },
    'dt': '',
    'sys': {
        'type': '',
        'id': '',
        'country': '',
        'sunrise': '',
        'sunset': ''
    },
    'timezone': '',
    'id': '',
    'name': '',
    'cod': ''
}

# API response field descriptions
API_RESPONSE_FIELD_DESCRIPTIONS = {
    'coord': {
        'lon': 'City geo location, longitude',
        'lat': 'City geo location, latitude'
    },
    'weather': [
        {   
            'id': 'Weather condition id',
            'main': 'Group of weather parameters (Rain, Snow, Extreme etc.)',
            'description': 'Weather condition within the group',
            'icon': 'Weather icon id'
        }
    ],
    'base': 'Internal parameter',
    'main': {
        'temp': 'Temperature. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.',
        'feels_like': 'Temperature. This temperature parameter accounts for the human perception of weather. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.',
        'temp_min': 'Minimum temperature at the moment. This is minimal currently observed temperature (within large megalopolises and urban areas). Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.',
        'temp_max': 'Maximum temperature at the moment. This is maximal currently observed temperature (within large megalopolises and urban areas). Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.',
        'pressure': 'Atmospheric pressure (on the sea level, if there is no sea_level or grnd_level data), hPa',
        'humidity': 'Humidity, %',
        'sea_level': 'Atmospheric pressure on the sea level, hPa',
        'grnd_level': 'Atmospheric pressure on the ground level, hPa'
    },
    'visibility': 'Average visibility, metres',
    'wind': {
        'speed': 'Wind speed. Unit Default: metre/sec, Metric: metre/sec, Imperial: miles/hour.',
        'deg': 'Wind direction, degrees (meteorological)',
        'gust': 'Wind gust. Unit Default: metre/sec, Metric: metre/sec, Imperial: miles/hour'
    },
    'clouds': {
        'all': 'Cloudiness, %'
    },
    'dt': 'Time of data calculation, unix, UTC',
    'sys': {
        'type': 'Internal parameter',
        'id': 'Internal parameter',
        'country': 'Country code (GB, JP etc.)',
        'sunrise': 'Sunrise time, unix, UTC',
        'sunset': 'Sunset time, unix, UTC'
    },
    'timezone': 'Shift in seconds from UTC',
    'id': 'City ID',
    'name': 'City name',
    'cod': 'Internal parameter'
}

# API response field examples
API_RESPONSE_FIELD_EXAMPLES = {
    'coord': {
        'lon': 139,
        'lat': 35
    },
    'weather': [
        {
            'id': 800,
            'main': 'Clear',
            'description': 'clear sky',
            'icon': '01n'
        }
    ],
    'base': 'stations',
}

# Call the  OpenWeatherMap API
def call_api(city, country, units):

 
    # Try catch block to catch any exceptions
    # that may occur when calling the API
    # and return None if an exception occurs
    # so that the calling function can handle
    # the error
    try:
        # Do error checking on the input parameters 
        if city == None or country == None or units == None:
            return None
        
        # Check if the units parameter is valid
        if units != 'metric' and units != 'imperial':
            return None
        
        # Check if the city parameter is valid
        if len(city) == 0:
            return None
        
        # Check if the country parameter is valid
        if len(country) == 0:
            return None
        
        # Build the URL
        url = API_URL + '?q=' + city + ',' + country + '&units=' + units + '&appid=' + API_KEY

        # Call the API
        response = requests.get(url)

        # Check the response status code
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None
    finally:
        pass

    
# Get the API response field types
def get_api_response_field_types():
    return API_RESPONSE_FIELD_TYPES

# Get the API response field values 
def get_api_response_field_values():
    return API_RESPONSE_FIELD_VALUES

# Get the API response field units
def get_api_response_field_units():
    return API_RESPONSE_FIELD_UNITS

# Get the API response field descriptions
def get_api_response_field_descriptions():
    return API_RESPONSE_FIELD_DESCRIPTIONS

# Get the API response field examples
def get_api_response_field_examples():
    return API_RESPONSE_FIELD_EXAMPLES


# main function with argument parsing
def main(argv):

    #Check if the number of arguments is correct
    # and print an error message if it is not
    # and return from the function
    if len(argv) != 3:
        print('Error: Invalid number of arguments')
        return
    
    # Print the input parameters
    print('Input parameters:')
    print(argv)
    print('')
    print('')

       
    #Error checking on the input parameters
    if argv[0] == None or argv[1] == None or argv[2] == None:
        print('Error: Invalid input parameters')
        return
    
    #  Get the first argument , second argument and third argument
    #  from the command line
    arg0 = argv[0]
    arg1 = argv[1]
    arg2 = argv[2]

    
    # Call the API
    response = call_api(arg0, arg1, arg2)
    print(response)

if __name__ == "__main__":
    import sys

    # Call the main function
    main(sys.argv[1:])





