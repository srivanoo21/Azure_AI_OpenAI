import os
import re
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load all the environment variables
load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") 
apikey = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = os.getenv("DEPLOYMENT_NAME")

     
client = AzureOpenAI(
    azure_endpoint = endpoint,
    api_key = apikey,
    api_version="2024-02-01",
)


# This will correspond to the custom name you chose for your deployment when you deployed a model.
# Use a gpt-35-turbo-instruct deployment.


context = 'CREATE TABLE retail_sales ("Revenue" numeric, "Cost of Goods" numeric, "Gross Profit" numeric, "Quantity Sold" numeric, "Discount" numeric, "Revenue Percentage Increase" numeric, "Sale Date" date, "Store Type" text, "Store Region" text, "Store Name" text, "Product Category" text, "Product Subcategory" text, "Country" text, "State" text, "City" text, "Sale Date Year" numeric, "Sale Date Quarter" numeric, "Sale Date Month" numeric, "Sale Date Day" numeric, "Sale Date" date, "Store Type" text, "Store Region" text, "Store Name" text, "Product Category" text, "Product Subcategory" text, "Country" text, "State" text, "City" text, "Sale Date Year" numeric, "Sale Date Quarter" numeric, "Sale Date Month" numeric, "Sale Date Day" numeric);'
question = "Revenue and Gross Profit by Sale Date Year and Sale Date Quarter"
error_message = ""
categorical_columns = []

# Send a completion call to generate an answer
prompt = [
            f"[INST] Write SQLite query to answer the following question given the database schema and possible values for categorical columns (if applicable), considering all date fields in 'YYYY-MM-DD' format. Please wrap your code answer using `sql` and make sure to end the query with a semicolon. Schema: {context} Question: {question} **Possible values for categorical columns are {categorical_columns}.** If there is no match found, please return NULL. Also, ensure to use GROUP BY clause wherever 'by', 'per', or 'for each' keyword is mentioned. {error_message} [/INST] Here is the SQLite query to answer the question: {question}:"
        ]

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

#print(response.choices[0].text)

query = response.choices[0].text

# Use regex to find the SELECT statement
match = re.search(r'SELECT\b(.*?)(?=\bFROM\b)', query, re.IGNORECASE)

print("Generated SQL query is: \n")
if match:
    select_statement = 'SELECT ' + match.group(1).strip()  # Add a space after 'SELECT'
    print(select_statement)
else:
    print("No SELECT statement found.")