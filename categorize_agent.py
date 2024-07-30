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



def Categorize_agent(email):
    messages = [
        {
            "role": "system",
            "content": f"""Conduct a comprehensive analysis of the email provided and categorize it into \
            one of the following categories:
            flow of finding should be 
            if price_inquiry
            elif customer_complaint
            elif product_inquiry
            elif cutsomer_feedback
            elif faq
            else 
            off_topic
            - price_inquiry: used when someone is asking for information about pricing of product and any details regarding product only.
            - customer_complaint: used when someone is complaining about something
            - product_inquiry: used when someone is asking for information about a product feature, benefit, service, or availability of the product
            - customer_feedback: used when someone is giving feedback about a product
            - off_topic: used when it doesn't relate to any other category and which is out of other category.
            - faq: used when someone is asking frequently asked questions about film equipment, such as types of cameras, lenses, lighting, audio equipment, accessories, or post-production software. This includes questions about product comparisons, differences between products, and how to use products.

            Examples of keywords and phrases that should be categorized as 'faq':
            - "types of cameras"
            - "difference between full-frame and crop sensor cameras"
            - "choose the right camera"
            - "types of lenses"
            - "choose the right lens"
            - "types of lights"
            - "set up basic three-point lighting"
            - "types of microphones"
            - "choose the right microphone"
            - "essential accessories for film production"
            - "maintain my film equipment"
            - "software for editing film"
            - "color grading"
            and also any question related to comparison

            STRICTLY Output a single category only, DONT ADD ANY EXTRA SENTENCES
            A single category for the type of email from the types ('price_inquiry', 'customer_complaint', 'product_inquiry', 'customer_feedback', 'off_topic', 'faq') \
            e.g., of output format: 
            'price_inquiry'


"""        },
        {
            "role": "user",
            "content": email,
        }
    ]
    

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tool_choice="required",
        max_tokens=4096
    )

    # Handle function calls if any in the initial response
    response_message = response.choices[0].message
    return response_message




