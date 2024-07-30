import os
import sqlite3
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Ensure your API key is set correctly
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not set. Please set it in the .env file and try again.")

client = Groq(api_key=api_key)
MODEL = 'llama3-8b-8192'
DB_PATH = 'equipment_rental.db'

def search_database(query):
    """ Retrieve data from SQLite for user query."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return json.dumps({"results": results})

def Reviewer_agent(user_prompt):
    messages = [
        {
            "role": "system",
            "content": """You are a Friendly review agent if the review of the user are 
            Positive Reviews: Thank the sender and encourage them to share their experience on social media
            social media link to tag in post and mention their review is -"https://www.linkedin.com/in/mathavansg/"
            if its -
            Negative Reviews:Responded the user that issue has been Escalated to the CRM system for follow-up with a phone call from customer service and offer a gift voucher in the reply
            Gift Voucher-"Happy shopping again".

"""        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=4096
    )

    # Handle function calls if any in the initial response
    response_message = response.choices[0].message


    return response_message