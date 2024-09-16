import os
import requests
from openai import AzureOpenAI
# from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint_url = "https://myaudiotranscript123.openai.azure.com/"
api_key = "8413afec5dcd4031b034399c99142a68"
whisper_model = "audiototext"
chat_model="chatmodel"
region="northcentralus"

final_url = f"{endpoint_url}/openai/deployments/{whisper_model}/audio/transcriptions?api-version=2023-09-01-preview"

headers = {
    "api-key": api_key,
}

file_path = r"D:\\Data_Science_stuff\\Data_Science_notes\\ineuron\\Azure_AI\\Azurecode\\voicedata\\voice.mp4"

# endpoint = os.getenv("ENDPOINT_URL", "https://myaudiototranscript1.openai.azure.com/")
# deployment = os.getenv("DEPLOYMENT_NAME", "chatmodel1")

# token_provider = get_bearer_token_provider(
#     DefaultAzureCredential(),
#     "https://cognitiveservices.azure.com/.default")
      
with open(file_path, "rb") as file:
    files = {"file": (os.path.basename(file_path), file, "application/octet-stream")}

    final_response = requests.post(final_url, headers=headers, files=files).json()
    print(final_response)

    user_prompt = final_response['text']

    client = AzureOpenAI(
        azure_endpoint = endpoint_url,
        api_key = api_key,
        #azure_ad_token_provider=token_provider,
        api_version = "2024-05-01-preview",
    )
        
    completion = client.chat.completions.create(
        model=chat_model,
        messages= [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_prompt}
        ],
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    print(completion.choices[0].message.content)