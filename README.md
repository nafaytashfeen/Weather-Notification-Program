# Weather-Notification-Script

The Weather Notification Program is a Python-based application designed to provide users with tailored weather notifications. By leveraging the OpenWeatherMap API, the program retrieves current weather conditions for a specified city, including temperature, wind speed, and sky conditions. It then generates a personalized message based on these conditions and sends it to users through the Pushover API.


Features:

 - City-Based Weather Retrieval: Fetches the current weather conditions for a user-specified city.

- Personalized Messaging: Generates customized weather notifications based on temperature, wind speed,  and sky conditions.

- Notification Sending: Sends notifications to users via text using the Pushover API.


How it Works:

- Geocoding: Retrieve geographic data (latitude and longitude) for the specified city using the OpenWeatherMap Geocoding API.

- Weather Data: Retrieve the appropriate weather data for the previously aquired geographical data. This weather data includes temperature, wind conditions, and sky conditions

- Message Generation: Generate a weather related message using either the OpenAI API or by using the function with pre-set messages (function <messages>)

- Send Notifications: After creating a message, send it to the users phone through the Pushover API, which will require the user to download the Pushover App


How to use:

1. Install Dependancies: Download the required dependancies found in the requirements.txt file: (pip install -r requirements.txt)

2. API Keys: Create/Signup for API keys with OpenWeatherMap and Pushover and optionally OpenAI

3. Configure API Keys:
    - OpenWeatherMap: Input your API key in weathernotification.py on lines <16>, <23>, and <56>.
    - Pushover: Input your API token and user in weathernotification.py on lines <191> and <192>.
    - (Optional) OpenAI: Input your API key in weathernotification.py on line <85>.


4. Run the Script: Call the function <create_and_send_message> with the appropriate parameters to get the program to work

6. (Optional) Automation: Automate running the script using AWS or other automation tools


Required API keys from: 
    - https://openweathermap.org/api
    - https://pushover.net/api

Optional API keys from:
    - https://openai.com/api/