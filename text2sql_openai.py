import os
import re
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_community.chat_models import ChatOpenAI
from langchain import LLMChain  

# Load all the environment variables
load_dotenv()

# Get OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Model name: GPT-4, GPT-3.5-turbo, or any other available models
model_name = "gpt-3.5-turbo"  # or "gpt-4"

# Initialize the OpenAI LLM using LangChain
llm = ChatOpenAI(temperature=0, max_tokens=150, openai_api_key=openai_api_key, model=model_name)

context = 'CREATE TABLE retail_sales ("Revenue" numeric, "Cost of Goods" numeric, "Gross Profit" numeric, "Quantity Sold" numeric, "Discount" numeric, "Revenue Percentage Increase" numeric, "Sale Date" date, "Store Type" text, "Store Region" text, "Store Name" text, "Product Category" text, "Product Subcategory" text, "Country" text, "State" text, "City" text, "Sale Date Year" numeric, "Sale Date Quarter" numeric, "Sale Date Month" numeric, "Sale Date Day" numeric);'
question = "Revenue and Gross Profit by Sale Date Year and Sale Date Quarter"
error_message = ""
categorical_columns = []

# Prepare the prompt
prompt = '''
f"[INST] Write SQLite query to answer the following question given the database schema and possible values for categorical columns (if applicable), considering all date fields in 'YYYY-MM-DD' format. Please wrap your code answer using `sql` and make sure to end the query with a semicolon. Schema: {context} Question: {question} **Possible values for categorical columns are {categorical_columns}.** If there is no match found, please return NULL. Also, ensure to use GROUP BY clause wherever 'by', 'per', or 'for each' keyword is mentioned. {error_message} [/INST] Here is the SQLite query to answer the question: {question}:"
'''


prompt_template = PromptTemplate(
    input_variables = ["context", "question", "categorical_columns", "error_message"],
    template = prompt
)

# Initialize the LLMChain with the prompt template and the LLM
llm_chain = LLMChain(llm=llm, prompt=prompt_template)

# Run the chain with the context and user query to generate the SQL
sql_query = llm_chain.invoke({
    "context": context,
    "question": question,
    "categorical_columns": categorical_columns,
    "error_message": error_message
})

# Extract the SQL query from the 'text' key
sql_query_with_markers = sql_query['text']
sql_query_pattern = r'```sql\n(.*?)\n```'
match = re.search(sql_query_pattern, sql_query_with_markers, re.DOTALL)

if match:
    sql_query = match.group(1)  # Extract the SQL part
    print("\nExtracted SQL Query:\n")
    print(sql_query)
else:
    print("SQL query not found in output.")