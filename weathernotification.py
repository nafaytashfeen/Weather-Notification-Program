import requests
import openai


def get_geo_codes(city_name: str, country_code: str, state_code: str="") -> tuple[str, str]:
    """
    This function gets the Long and Lat given the <city_name> and <country_code>, and optionally, 
    the <state_code> if the city is in the US
    """
    base_url = "http://api.openweathermap.org/geo/1.0/direct"

    if state_code == "":
        query_params = {
            'q': f"{city_name},{country_code}",
            'limit': 1,
            'appid': "your-API-key-goes-here"
        }

    else:
        query_params = {
            'q': f"{city_name},{state_code},{country_code}",
            'limit': 1,
            'appid': "your-API-key-goes-here"
        }


    response = requests.get(base_url, params=query_params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse and return the JSON data
        data = response.json()
        latitude = data[0]['lat']
        longtitude = data[0]["lon"]


        return latitude, longtitude

    else:
        # Handle error
        print(f"Error: {response.status_code}")
        return None


def get_weather(geo_location: tuple[float, float]) -> tuple:
    """
    This function takes in a tuple with the latitude and longtitude of a city and returns the 
    appropriate weather conditions of that city so that the <message> function can be called
    to send the user a message based on the weather
    """
    base_url = "https://api.openweathermap.org/data/3.0/onecall"

    query_params = {
        "lat": geo_location[0],
        "lon": geo_location[1],
        "appid": "your-API-key-goes-here",
        "units": "metric"
    }

    response = requests.get(base_url, params=query_params)
    # Make the API Call

    if response.status_code == 200:
        data = response.json()
        # print(data)
        temperature = data["current"]['temp']
        wind_speed = data['current']['wind_speed']
        sky_conditions = data['current']['weather'][0]['main'].lower()

        return temperature, wind_speed, sky_conditions
    
    else:
        # Handle error
        print(f"Error: {response.status_code}")
        return None


def generated_message(weather: tuple[str]) -> str:
    """
    This function calls the OpenAI API and generates a short message 
    based on the temperature, wind speed and the sky conditions.
    """
    temperature, wind_speed, sky_conditions = weather

    openai.api_key = 'your-API-key-goes-here'

    # Define the prompt and other parameters for the completion
    response = openai.Completion.create(
    engine="gpt-3.5-turbo",  # You can use other engines like "gpt-3.5-turbo"
    prompt=f"Generate a short message for a user based on the following weather conditions, {temperature}, {wind_speed}, {sky_conditions}, the message should follow this type of format, eg: The temperature is {temperature}. It's cold, windy, and rainy/snowy today. Don't forget your waterproof winter jacket. This is simply an example, adjust the message based on conditions",
    max_tokens=2,  # Adjust the number of tokens as needed
    temperature=0.7,  # Controls the creativity
    n=1,  # Number of responses to generate
    stop=None  # You can set stop sequences here
    )

    generated_text = response.choices[0].text.strip()
    return generated_text


def message(weather: tuple[str]) -> str:
    """
    Formulate a message based on the temperature, wind speed and the sky conditions.
    """
    temperature, wind_speed, sky_conditions = weather

    if temperature <= -20:
        message = f"The temperature is {temperature}. It is extremely cold today. Wear a warm winter jacket."

    elif -20 < temperature <= -10 and wind_speed > 10 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's cold, windy, and rainy/snowy today. Don't forget your waterproof winter jacket."

    elif -20 < temperature <= -10 and wind_speed >= 0 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's cold and rainy/snowy today. Dress warmly and consider bringing an umbrella."

    elif -20 < temperature <= -10 and 0 < wind_speed <= 10 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's cold today with light wind and rain/snow. Wear a warm jacket and carry an umbrella."

    elif -20 < temperature <= -10 and wind_speed > 10 and ('rain' not in sky_conditions and 'snow' not in sky_conditions):
        message = f"The temperature is {temperature}. It's cold and windy today. Wear a heavy jacket to stay warm."

    elif -20 < temperature <= -10 and wind_speed >= 0 and ('rain' not in sky_conditions and 'snow' not in sky_conditions):
        message = f"The temperature is {temperature}. It's cold today. Dress warmly with layers."

    elif -10 < temperature <= 0 and wind_speed > 10 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's chilly, windy, and rainy/snowy today. Wear a waterproof jacket and dress in layers."

    elif -10 < temperature <= 0 and wind_speed >= 0 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's chilly and rainy/snowy today. Dress warmly and consider bringing an umbrella."

    elif -10 < temperature <= 0 and 0 < wind_speed <= 10 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's chilly today with light wind and rain/snow. Wear a jacket and carry an umbrella."

    elif -10 < temperature <= 0 and wind_speed > 10 and ('rain' not in sky_conditions and 'snow' not in sky_conditions):
        message = f"The temperature is {temperature}. It's chilly and windy today. Wear a jacket to stay warm."

    elif -10 < temperature <= 0 and wind_speed >= 0 and ('rain' not in sky_conditions and 'snow' not in sky_conditions):
        message = f"The temperature is {temperature}. It's chilly today. Dress warmly with layers."

    elif 0 < temperature <= 10 and wind_speed > 10 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's cool, windy, and rainy. Wear a jacket and carry an umbrella."

    elif 0 < temperature <= 10 and wind_speed >= 0 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's cool and rainy today. Dress warmly and consider bringing an umbrella."

    elif 0 < temperature <= 10 and 0 < wind_speed <= 10 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's cool today with light wind and rain/snow. Wear a light jacket and carry an umbrella."

    elif 0 < temperature <= 10 and wind_speed > 10 and ('rain' not in sky_conditions and 'snow' not in sky_conditions):
        message = f"The temperature is {temperature}. It's cool and windy today. Wear a light jacket to stay warm."

    elif 0 < temperature <= 10 and wind_speed >= 0 and ('rain' not in sky_conditions and 'snow' not in sky_conditions):
        message = f"The temperature is {temperature}. It's cool today. Dress warmly with layers."
    
    elif 10 < temperature <= 20 and wind_speed > 10 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's mild, windy, and rainy/snowy today. Wear a jacket and bring an umbrella."

    elif 10 < temperature <= 20 and wind_speed >= 0 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's mild and rainy/snowy today. Dress warmly and consider bringing an umbrella."

    elif 10 < temperature <= 20 and 0 < wind_speed <= 10 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's mild today with light wind and rain/snow. Bring a light jacket and an umbrella."

    elif 10 < temperature <= 20 and wind_speed > 10 and ('rain' not in sky_conditions and 'snow' not in sky_conditions):
        message = f"The temperature is {temperature}. It's mild and windy today. Wear a light jacket to stay comfortable."

    elif 10 < temperature <= 20 and wind_speed >= 0 and ('rain' not in sky_conditions and 'snow' not in sky_conditions):
        message = f"The temperature is {temperature}. It's mild today. Dress comfortably with light layers."

    elif 20 < temperature <= 30 and wind_speed > 10 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's warm, windy, and rainy/snowy today. Dress lightly and bring an umbrella."

    elif 20 < temperature <= 30 and wind_speed >= 0 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's warm and rainy/snowy today. Dress comfortably and consider bringing an umbrella."

    elif 20 < temperature <= 30 and 0 < wind_speed <= 10 and ('rain' in sky_conditions or 'snow' in sky_conditions):
        message = f"The temperature is {temperature}. It's warm today with light wind and rain/snow. Dress lightly and bring an umbrella."

    elif 20 < temperature <= 30 and wind_speed > 10 and ('rain' not in sky_conditions and 'snow' not in sky_conditions):
        message = f"The temperature is {temperature}. It's warm and windy today. Dress comfortably and enjoy the weather."

    else: #elif 20 < temperature <= 30 and wind_speed >= 0 and ('rain' not in sky_conditions and 'snow' not in sky_conditions):
        message = f"The temperature is {temperature}. It's warm today. Dress comfortably and enjoy the pleasant conditions."

    return message            


def send_message(message) -> None:
    url = "https://api.pushover.net/1/messages.json"
    data = {
        'token': "your-token-goes-here",
        'user': "your-user-goes-here",
        'message': message,
    }
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status}")
        print("Response content:")
        print(response.read().decode("utf-8"))
        

def create_and_send_message(city_name: str, country_code: str, generated_message: bool=False, state_code: str="") -> bool:
    """
    This function goes through the process of getting the weather data 
    for the input city and creates and sends a message to the clients phone. If 
    everything goes smoothly, the function will return True, else False. 
    
    The <state_code> parameter is optional and only needed if the city is in the US.

    The <generated_message> parameter should be True if the client wants an AI generated 
    message, else it is False by default .
    """
    try:
        loc_data = get_geo_codes(city_name, country_code, state_code)
        weather_data = get_weather(loc_data)

        if generated_message:
            message_to_send = generated_message(weather_data)
        
        else:
            message_to_send = message(weather_data)

        send_message(message_to_send)

        return True
    
    except:
        # In case somethig went wrong in the above steps
        print("Error")
        return False
    

if __name__ == "__main__":
    # Sample usage of the function <create_and_send_message>, keep in mind the user must put in 
    # their own API keys for the functions <get_geo_codes>, <get_weather>, <generated_message>,
    # and <send_message>.
    
    city = "Toronto"
    country = "CA" # Country code must be in the ISO 3166 format

    # create_and_send_message(city, country, True)