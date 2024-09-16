import os
from openai import AzureOpenAI

endpoint = "https://crashname.openai.azure.com/"
apikey = "9478c4f8d8784a278fc9ef6afbeef950"

client = AzureOpenAI(
    api_key=apikey,
    api_version="2024-02-01",
    azure_endpoint=endpoint
)

# This will correspond to the custom name you chose for your deployment when you deployed a model.
# Use a gpt-35-turbo-instruct deployment.
deployment_name = "crashchatengine"

# Send a completion call to generate an answer
prompt = "hi, what is delhi, what is Delhi famous for, how people survive in Delhi, Delhi news, Delhi information, Delhi history, Delhi travel guide, Delhi travel details, delhi travel information, delhi tourist guide, Delhi politics, Delhi geography, Delhi food, Delhi festival, New Delhi india, Delhi Tourism, Delhi Tour and Travels, Places to visit in Delhi india\n\nTags: ncr , panipat in 2020 population estimates\n\nFacebook Is Working On Its Own Snapchat-esque Camera App\n"
response = client.completions.create(
    model=deployment_name,
    prompt=prompt,
    temperature=0.9,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["Human:","AI:"]
)

print(prompt + response.choices[0].text)
