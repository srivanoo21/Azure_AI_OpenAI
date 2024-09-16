import os
from openai import AzureOpenAI
#from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://crashname.openai.azure.com/"
apikey = "9478c4f8d8784a278fc9ef6afbeef950"

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
      
completion = client.chat.completions.create(
    model="crashchatengine",
    messages= [
    {
      "role": "user",
      "content": "how many stars in the universe?"
    }],
    max_tokens=800,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)
print(completion.to_json())