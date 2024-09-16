import os
import requests
import json
from openai import AzureOpenAI
#from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://crashinstance123.openai.azure.com/"
apikey = "4300381980904acb8c766d70021d08ed"
     

client = AzureOpenAI(
    azure_endpoint = endpoint,
    api_key = apikey,
    api_version = "2024-05-01-preview",
)


initial_response  = client.chat.completions.create(
    model="crashdeploy",
    messages= [
         {"role": "system", "content": "You are an assistant that helps people retrieve real-time weather."},
         {"role": "user", "content": "how is the weather in mumbai?"}
         ],
    #functions=functions,
    max_tokens=800,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)

print(initial_response.to_json())

