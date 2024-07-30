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

def Database_agent(user_prompt):
    messages = [
        {
            "role": "system",
            "content": """You are a data retrieval assistant. Use the search_database function to retrieve data.
                          Do not ask questions. Respond with data from the 'equipment' table based on user queries.
                          Structure of the 'equipment' table: id, name, type, availability, price.
                          Output should be only the query no extra character
                          
                          sample data-
                          ('Camera', 'Video', 'Available', 1200.00),
                        ('Microphone', 'Audio', 'Unavailable', 150.00),
                        ('Tripod', 'Accessory', 'Available', 300.00),
                        ('Lighting Kit', 'Lighting', 'Available', 500.00)
                        
                        Strictly donot create any '\' character in output. 

"""        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_database",
                "description": "Retrieve data from SQLite for user query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The SQL query to execute for retrieving data.",
                        }
                    },
                    "required": ["query"],
                },
            },
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )
    print("r\n",response)

    # Handle function calls if any in the initial response
    response_message = response.choices[0].message


    if response_message.tool_calls:
        available_functions = {
            "search_database": search_database,
        }


        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                query=function_args.get("query")
            )
            print(function_response)
            
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
            updated_system_message={
            "role": "system",
            "content": """Your a Customer Friendly agent,Respond with the friendly tone detailed  data with all necessary columns from the 'equipment' table 
            but just the record and not the whole table and also give the record in json structure and also  If user requested particular item available, reply with the item's record.
            If not available, suggest similar available items
"""        }
            messages[0]=updated_system_message

           
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return second_response.choices[0].message.content




