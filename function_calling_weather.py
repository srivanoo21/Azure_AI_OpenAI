import os
import requests
import json
import re
from openai import AzureOpenAI
#from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://crashinstance123.openai.azure.com/"
apikey = "4300381980904acb8c766d70021d08ed"

# endpoint = os.getenv("ENDPOINT_URL", "https://crashname.openai.azure.com/")
# deployment = os.getenv("DEPLOYMENT_NAME", "crashchatengine")

# token_provider = get_bearer_token_provider(
#     DefaultAzureCredential(),
#     "https://cognitiveservices.azure.com/.default")
      
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key = apikey,
    #azure_ad_token_provider=token_provider,
    api_version="2024-05-01-preview",
)

# function format
functions=[
    {
        "name":"getWeather",
        "description":"Retrieve real-time weather information/data about a particular location/place",
        "parameters":{
            "type":"object",
            "properties":{
                "location":{
                    "type":"string",
                    "description":"the exact location whose real-time weather is to be determined",
                },
                
            },
            "required":["location"]
        },
    }
] 
      

# function for fetching weather
def get_weather(location):
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + location  + "&appid=a6d4f664b69c776acf994fd78496ed3a"
    response=requests.get(url)
    get_response=response.json()
    latitude=get_response['coord']['lat']
    longitude = get_response['coord']['lon']
    print(f"latitude: {latitude}")
    print(f"longitude: {longitude}")

    url_final ="https://api.openweathermap.org/data/2.5/weather?lat="+ str(latitude) + "&lon=" + str(longitude) + "&appid=a6d4f664b69c776acf994fd78496ed3a"
    final_response = requests.get(url_final)
    final_response_json = final_response.json()
    weather=final_response_json['weather'][0]['description']
    print(f"weather condition: {weather}")




initial_response = client.chat.completions.create(
    model="crashanoop",
    messages= [
         {"role": "system", "content": "You are an assistant that helps people retrieve real-time weather."},
         {"role": "user", "content": "how is the weather in mumbai?"}
         ],
    functions=functions,
    max_tokens=800,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)

print("**********************Initial Response************************************************")
print("\n")
print(initial_response.choices[0].message.function_call.arguments)
print("\n")

function_argument = json.loads(initial_response.choices[0].message.function_call.arguments)
location = function_argument['location']

if (location):
    print(f"city: {location}")
    get_weather(location)


