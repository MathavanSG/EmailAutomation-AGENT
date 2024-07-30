from utils import authenticate_gmail, get_emails,create_message,send_message,extract_subject_and_body
from crewai import Crew, Task, Process
from categorize_agent import Categorize_agent
from data_agent import Database_agent
from reviewer_agent import Reviewer_agent
from rag_agent  import get_rag_output
from crm import add_customer_data
from email_writer import email_writer_agent
def generate_sample_emails():
    return [
        {
            'id': '1',
            'subject': 'Inquiry about Camera Pricing',
            'body': 'Hello, I would like to know the price of your camera. Thanks!'
        },
        {
            'id': '2',
            'subject': 'Issue with Microphone',
            'body': 'Hi, I recently purchased a microphone from your store, and it stopped working after a week. Please assist.'
        },
        {
            'id': '3',
            'subject': 'Feedback on Lighting Kit',
            'body': 'Hello, I just wanted to say that I am very happy with the lighting kit I bought from you. It works perfectly!'
        },
        {
            'id': '4',
            'subject': 'Questions about how to choose the right microphone',
            'body': 'Hi, I am new to filmmaking Could you provide some insights about how to choose the right microphone?'
        },
        {
            'id': '5',
            'subject': 'Questions about health',
            'body': 'Hi, Can i know about the  md health?'
        }
    ]



def main():
    """
    To fetch email direct from gmail-
    # Authenticate and get the Gmail service
    service = authenticate_gmail()
    
    # Specify the number of emails to retrieve
    max_results = 2  # You can adjust this number as needed

    # Retrieve emails from Gmail
    emails = get_emails(service, max_results=max_results)
    """
    # For now, we use sample emails
    emails = generate_sample_emails()
    inquiry_handle_request = ['price_inquiry', 'product_inquiry']
    feedback_request = ['customer_complaint', 'customer_feedback']

    for email in emails:
        print(f"Processing email with subject: {email['subject']}")
        print(email['body'])
        categorized_result = Categorize_agent(email['body'])
        print("Category-",categorized_result.content.strip("'"))
        response = None

        if categorized_result.content.strip("'") in inquiry_handle_request:
            response = Database_agent(email['body'])
        elif categorized_result.content.strip("'") in feedback_request:
            response = Reviewer_agent(email['body'])
        elif categorized_result.content.strip("'") == 'faq':
            response = get_rag_output(email['body'])
        else:
            response = add_customer_data(email)
        
        if hasattr(response, 'content'):
            response_content = response.content
        else:
            response_content = response

        # Use the email_writer_agent to generate the email subject and body
        email_response = email_writer_agent(email['body'], response_content)
        subject, body = extract_subject_and_body(email_response)
        print("____________________")
        print('subject:\n',subject)

        print('body: \n',body)
        print("____________________")

if __name__ == '__main__':
    main()