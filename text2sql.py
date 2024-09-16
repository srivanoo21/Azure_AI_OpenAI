import os
from openai import AzureOpenAI

endpoint = "https://text2sql123.openai.azure.com/"
apikey = "84c615621cb745f0b1022c12ba721190"
     
client = AzureOpenAI(
    azure_endpoint = endpoint,
    api_key = apikey,
    api_version="2024-02-01",
)


# This will correspond to the custom name you chose for your deployment when you deployed a model.
# Use a gpt-35-turbo-instruct deployment.
deployment_name = "text2sql"

# Send a completion call to generate an answer
prompt = "['[INST] Write an SQLite query to answer the following question using the provided database schema. Make sure all date fields are in \'YYYY-MM-DD\' format. Wrap your SQL code answer using `sql` and end the query with a semicolon. Schema: CREATE TABLE empdata (\"PIN\" text, \"LASTNAME\" text, \"FIRSTNAME\" text, \"MIDINITIAL\" text, \"DIV\" text, \"DEPT\" text, \"JOBCLASS\" text, \"TITLE\" text, \"SALARY\" numeric, \"HIREDATE\" date, \"AREA\" text); Question: which AREA  has highest SALARY  **Possible values for categorical columns are {}.** If no match is found, return NULL. Use the GROUP BY clause whenever \'by\', \'per\', or \'for each\' is mentioned. **Do not use aliases or abbreviations for column names in the SQL query. Use the full column names only.** [/INST] Here is the SQLite query to answer the question: which AREA  has highest SALARY :']]\n\nSELECT AREA\nFROM empdata\nGROUP BY AREA\nHAVING SALARY = MAX(SALARY)"
response = client.completions.create(
    model=deployment_name,
    prompt=prompt,
    temperature=0,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["#",";"]
)

print(prompt + response.choices[0].text)
