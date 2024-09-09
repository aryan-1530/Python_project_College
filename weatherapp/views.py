from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    # Get city from POST request or set default
    city = request.GET.get('city', 'amritsar')
    print(city)
    
    # API keys (replace with actual keys)
    weather_api_key = "U2WPZE57STC6C46ZC6RDGVZ8Z"  # Visual Crossing API key
    google_api_key = 'your_google_api_key'
    search_engine_id = 'your_search_engine_id'

    # Get the current date and time
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    print(formatted_datetime)

    # Visual Crossing API URL with the current date and time
    weather_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{formatted_datetime}?key={weather_api_key}&include=current"
    
    # Google Custom Search API URL and parameters
    query = city + " 1920x1080"
    search_type = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={search_engine_id}&q={query}&searchType={search_type}&imgSize=xlarge"

    try:
        print("try block")
        #image_response = requests.get(city_url)
        #image_response.raise_for_status()  # Check for HTTP errors
        #image_data = image_response.json()

        # Ensure 'items' exists and has content
        #search_items = image_data.get("items")
        #image_url = search_items[0]['link'] if search_items else None
        
        # Fetch weather data from Visual Crossing API
        print("weather")
        weather_response = requests.get(weather_url)

        if weather_response:  # Check if response is not None
            weather_response.raise_for_status()  # Check for HTTP errors
            weather_data = weather_response.json()
            print("top")
            print(weather_data)
        else:
            print("Error: Could not retrieve weather data.")
            print("bottom")

        # Extract current weather details
        current_conditions = weather_data.get('currentConditions', {})
        description = current_conditions.get('conditions', 'No description available')
        icon = current_conditions.get('icon', 'clear-day')  # Default to 'clear-day' if no icon is provided
        temp_fahrenheit = current_conditions.get('temp', 'N/A')
        temp_celsius = (temp_fahrenheit - 32) * 5/9
        temp = round(temp_celsius, 2)

        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            #'image_url': image_url
        })

    except (requests.RequestException, KeyError, IndexError, ValueError) as e:
        # Handle API errors or missing data gracefully
        messages.error(request, 'Entered data is not available from the API')
        day = datetime.date.today()
        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': city,
            'exception_occurred': True
        })
