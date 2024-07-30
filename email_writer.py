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


def email_writer_agent(user_email,response):
    messages = [
        {
            "role": "system",
            "content": f"""You are a email writer agent You should write a email response to the user email content
            user email content: {user_email},
            response for the user email content: {response},

            based on the above information draft a friendly email to user donot add content, focus on the response for the user email content and beautify it.

            You need to output in a certain format-
            <subject> subject for the email </subject>
            <body> email body </body>
            YOUR STRICTLY INSTRUCTED TO OUTPUT ONLY IN THE ABOVE FORMAT AND NO EXTRA SPACE AND CHARACTER
            ALSO  STRICTLY ADD THE TAGS <subject></subject> and <body> </body>.

"""        },
        {
            "role": "user",
            "content": user_email,
        },
        {
            "role": "assistant",
            "content":response
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