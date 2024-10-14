import os
import re
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_community.chat_models import ChatOpenAI
from langchain import LLMChain  
import google.generativeai as genai


# Load all the environment variables
load_dotenv()

# Get API key from environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)

# Model name: gemini-pro'
model_name = "gemini-pro"


context = 'CREATE TABLE retail_sales ("Revenue" numeric, "Cost of Goods" numeric, "Gross Profit" numeric, "Quantity Sold" numeric, "Discount" numeric, "Revenue Percentage Increase" numeric, "Sale Date" date, "Store Type" text, "Store Region" text, "Store Name" text, "Product Category" text, "Product Subcategory" text, "Country" text, "State" text, "City" text, "Sale Date Year" numeric, "Sale Date Quarter" numeric, "Sale Date Month" numeric, "Sale Date Day" numeric);'
question = "Revenue and Gross Profit by Sale Date Year and Sale Date Quarter"
error_message = ""
categorical_columns = []

# Prepare the prompt
prompt = [
f"[INST] Write SQLite query to answer the following question given the database schema and possible values for categorical columns (if applicable), considering all date fields in 'YYYY-MM-DD' format. Please wrap your code answer using `sql` and make sure to end the query with a semicolon. Schema: {context} Question: {question} **Possible values for categorical columns are {categorical_columns}.** If there is no match found, please return NULL. Also, ensure to use GROUP BY clause wherever 'by', 'per', or 'for each' keyword is mentioned. {error_message} [/INST] Here is the SQLite query to answer the question: {question}:"
]


# Function to get response from Gemini model
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt[0], question])
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

response = get_gemini_response(question, prompt)
print("\nGenerated SQL query is: ")

# Remove leading and trailing whitespace
cleaned_output = re.sub(r'```sql|```', '', response)
cleaned_output.strip()  

print(cleaned_output)