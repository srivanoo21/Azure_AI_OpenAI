# Note: DALL-E 3 requires version 1.0.0 of the openai-python library or later
import os
from openai import AzureOpenAI
import json

endpoint = "https://crashname.openai.azure.com/"
apikey = "9478c4f8d8784a278fc9ef6afbeef950"

client = AzureOpenAI(
    api_version="2024-05-01-preview",
    azure_endpoint=endpoint,
    api_key=apikey,
)

result = client.images.generate(
    model="Dalle3", # the name of your DALL-E 3 deployment
    prompt="give me a image where boy is cycling and dancing",
    n=1
)

image_url = json.loads(result.model_dump_json())['data'][0]['url']

print(image_url)